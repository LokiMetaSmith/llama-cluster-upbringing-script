import os
import time
import logging
import asyncio
import json
import sqlite3
import uvicorn
import faiss
import numpy as np
import pickle
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import httpx
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Archivist")

# --- Configuration ---
DB_PATH = os.getenv("DB_PATH", os.path.expanduser("~/.config/pipecat/pypicat_memory.db"))
INDEX_DIR = os.getenv("INDEX_DIR", os.path.expanduser("~/.config/pipecat/archivist_data"))
PORT = int(os.getenv("ARCHIVIST_PORT", 8008))
CONSUL_HOST = os.getenv("CONSUL_HOST", "127.0.0.1")
CONSUL_PORT = int(os.getenv("CONSUL_PORT", 8500))
LLAMA_API_SERVICE_NAME = os.getenv("LLAMA_API_SERVICE_NAME", "llamacpp-rpc-api")

# Ensure index directory exists
os.makedirs(INDEX_DIR, exist_ok=True)

# Thread pool for blocking ops
executor = ThreadPoolExecutor(max_workers=2)

class Page(BaseModel):
    id: str
    header: str
    content: str
    timestamp: float

class DeepResearchRequest(BaseModel):
    query: str
    max_steps: int = 5

# --- Helper Classes ---

class LLMClient:
    def __init__(self, consul_host, consul_port, service_name):
        self.consul_host = consul_host
        self.consul_port = consul_port
        self.service_name = service_name
        self.base_url = None
        self.client = httpx.AsyncClient(timeout=60.0)

    async def close(self):
        await self.client.aclose()

    async def discover(self):
        url = f"http://{self.consul_host}:{self.consul_port}/v1/health/service/{self.service_name}?passing"
        try:
            resp = await self.client.get(url)
            if resp.status_code == 200:
                services = resp.json()
                if services:
                    svc = services[0]['Service']
                    self.base_url = f"http://{svc['Address']}:{svc['Port']}/v1"
                    logger.info(f"Discovered LLM at {self.base_url}")
        except Exception as e:
            logger.error(f"Service discovery failed: {e}")

    async def generate(self, prompt: str, temperature: float = 0.0) -> str:
        if not self.base_url:
            await self.discover()

        if not self.base_url:
            logger.error("LLM Service URL not found")
            return "Error: LLM Service Unavailable"

        try:
            resp = await self.client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": "gpt-3.5-turbo", # Placeholder model name
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature
                }
            )
            resp.raise_for_status()
            data = resp.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"LLM Call failed: {e}")
            return f"Error generating response: {e}"

# --- Memorizer ---

class Memorizer:
    def __init__(self, db_path: str, index_dir: str, llm_client: LLMClient):
        self.db_path = db_path
        self.index_dir = index_dir
        self.llm_client = llm_client
        # Use the same model as RAG tool/Memory Store for consistency
        self.embedding_model = SentenceTransformer('/opt/nomad/models/embedding/bge-large-en-v1.5')

        self.faiss_index_path = os.path.join(index_dir, "pages.faiss")
        self.bm25_index_path = os.path.join(index_dir, "pages.bm25")
        self.pages_store_path = os.path.join(index_dir, "pages.json")
        self.state_path = os.path.join(index_dir, "state.json")

        self.pages: Dict[str, Page] = {}
        self.page_ids_list: List[str] = [] # Maps FAISS index ID to Page ID

        self.faiss_index = None
        self.bm25 = None
        self.bm25_corpus = []

        self.last_processed_id = 0
        self.lightweight_memory = "No history yet."

        self._load_state()

    def _load_state(self):
        # Load Pages
        if os.path.exists(self.pages_store_path):
            with open(self.pages_store_path, 'r') as f:
                data = json.load(f)
                self.pages = {k: Page(**v) for k, v in data.items()}
                logger.info(f"Loaded {len(self.pages)} pages.")

        # Load FAISS
        if os.path.exists(self.faiss_index_path):
            self.faiss_index = faiss.read_index(self.faiss_index_path)
            logger.info("Loaded FAISS index.")
        else:
            self.faiss_index = faiss.IndexFlatL2(1024)

        # Load BM25
        if os.path.exists(self.bm25_index_path):
            with open(self.bm25_index_path, 'rb') as f:
                self.bm25, self.bm25_corpus = pickle.load(f)
            logger.info("Loaded BM25 index.")

        # Load State (and list)
        if os.path.exists(self.state_path):
            with open(self.state_path, 'r') as f:
                state = json.load(f)
                self.last_processed_id = state.get("last_processed_id", 0)
                self.lightweight_memory = state.get("lightweight_memory", "No history yet.")
                self.page_ids_list = state.get("page_ids_list", [])

                # Validation
                if len(self.page_ids_list) != self.faiss_index.ntotal:
                    logger.warning(f"Index mismatch! Pages: {len(self.page_ids_list)}, FAISS: {self.faiss_index.ntotal}")
                    # In a real system, we might trigger a rebuild. For now, assume state is correct or truncated.
                    if len(self.page_ids_list) < self.faiss_index.ntotal:
                        # Index is larger than list? This implies list was not saved or truncated.
                        # We can't recover easily without re-embedding everything.
                        pass
        else:
            # Fallback for migration if state file doesn't exist but pages do (shouldn't happen in fresh deploy)
            if not self.page_ids_list and self.pages:
                self.page_ids_list = list(self.pages.keys())

    def _save_state(self):
        with open(self.pages_store_path, 'w') as f:
            json.dump({k: v.model_dump() for k, v in self.pages.items()}, f)

        if self.faiss_index:
            faiss.write_index(self.faiss_index, self.faiss_index_path)

        with open(self.bm25_index_path, 'wb') as f:
            pickle.dump((self.bm25, self.bm25_corpus), f)

        with open(self.state_path, 'w') as f:
            json.dump({
                "last_processed_id": self.last_processed_id,
                "lightweight_memory": self.lightweight_memory,
                "page_ids_list": self.page_ids_list # Persist list order
            }, f)

    def _fetch_new_events(self):
        if not os.path.exists(self.db_path):
            if not hasattr(self, '_db_warned'):
                logger.warning(f"Database not found at {self.db_path}")
                self._db_warned = True
            return []

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, kind, content FROM events WHERE id > ? ORDER BY id ASC LIMIT 50", (self.last_processed_id,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            logger.error(f"DB Read Error: {e}")
            return []

    async def process_loop(self):
        logger.info("Starting Memorizer loop...")
        while True:
            try:
                # Run DB fetch in thread
                loop = asyncio.get_running_loop()
                events = await loop.run_in_executor(executor, self._fetch_new_events)

                if not events:
                    await asyncio.sleep(5)
                    continue

                chunk_content = ""
                end_id = self.last_processed_id

                for row in events:
                    eid, ts, kind, content = row

                    if kind == "audio":
                         end_id = eid
                         continue

                    chunk_content += f"[{kind}] {content}\n"
                    end_id = eid

                if not chunk_content.strip():
                    self.last_processed_id = end_id
                    await loop.run_in_executor(executor, self._save_state)
                    continue

                logger.info(f"Processing new events up to ID {end_id}")

                # 1. Update Lightweight Memory
                memo_prompt = f"""
                Current Memory Summary:
                {self.lightweight_memory}

                New Events to Integrate:
                {chunk_content}

                Task: Update the memory summary to include key new information. Maintain a coherent narrative. Keep it concise (under 500 words).
                """
                new_memory = await self.llm_client.generate(memo_prompt)
                if new_memory and not new_memory.startswith("Error"):
                    self.lightweight_memory = new_memory

                # 2. Generate Header
                header_prompt = f"""
                Context:
                {self.lightweight_memory}

                Content:
                {chunk_content[:2000]}

                Task: Generate a single sentence header/title that describes this interaction or event sequence.
                """
                header = await self.llm_client.generate(header_prompt)
                if not header or header.startswith("Error"):
                    header = f"Session ending at event {end_id}"

                # 3. Prepare Page
                page_id = str(end_id)
                page = Page(id=page_id, header=header, content=chunk_content, timestamp=time.time())

                # 4. Update Indices (Blocking, run in thread)
                def update_indices():
                    text_to_embed = f"{header}\n{chunk_content}"
                    embedding = self.embedding_model.encode([text_to_embed])[0]
                    self.faiss_index.add(np.array([embedding], dtype=np.float32))

                    tokenized_doc = text_to_embed.lower().split()
                    self.bm25_corpus.append(tokenized_doc)
                    self.bm25 = BM25Okapi(self.bm25_corpus)

                await loop.run_in_executor(executor, update_indices)

                # 5. Update Memory State (Main Thread)
                self.pages[page_id] = page
                self.page_ids_list.append(page_id)
                self.last_processed_id = end_id

                # Save
                await loop.run_in_executor(executor, self._save_state)

                logger.info(f"Archived page {page_id}. Total pages: {len(self.pages)}")

            except Exception as e:
                logger.error(f"Error in Memorizer loop: {e}", exc_info=True)
                await asyncio.sleep(30)

# --- Researcher ---

class Researcher:
    def __init__(self, memorizer: Memorizer, llm_client: LLMClient):
        self.memorizer = memorizer
        self.llm_client = llm_client

    async def deep_research(self, query: str, max_steps: int = 5) -> str:
        logger.info(f"Deep Research Request: {query}")

        # Current knowledge gathered
        collected_pages: Dict[str, Dict] = {}
        knowledge_summary = "No information gathered yet."

        step = 0
        while step < max_steps:
            step += 1
            logger.info(f"Research Step {step}/{max_steps}")

            # 1. Plan / Reflect
            # Check if we have enough info or need more searches
            plan_prompt = f"""
            User Request: {query}

            Current Knowledge Summary:
            {knowledge_summary}

            Memory Context (Lightweight):
            {self.memorizer.lightweight_memory}

            Task: Determine if the Current Knowledge is sufficient to answer the User Request.
            If YES, output JSON: {{"sufficient": true}}
            If NO, output JSON: {{"sufficient": false, "queries": ["query1", "query2"]}}

            Create specific queries to find missing details in the long-term memory.
            """

            plan_resp = await self.llm_client.generate(plan_prompt)
            sufficient = False
            queries = []

            try:
                clean_json = plan_resp.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)
                sufficient = data.get("sufficient", False)
                queries = data.get("queries", [])
            except:
                logger.warning("Failed to parse plan JSON. Proceeding with original query if first step.")
                if step == 1:
                    queries = [query]
                else:
                    sufficient = True # Bail out if we can't plan

            if sufficient:
                logger.info("Knowledge deemed sufficient.")
                break

            if not queries:
                logger.info("No queries generated, assuming done.")
                break

            # 2. Search (Parallel)
            logger.info(f"Executing queries: {queries}")
            for q in queries:
                # Run search in thread
                loop = asyncio.get_running_loop()
                results = await loop.run_in_executor(executor, self._search, q, 3)

                for res in results:
                    collected_pages[res['id']] = res

            # 3. Integrate / Summarize findings so far
            context_str = ""
            for pid, page_data in collected_pages.items():
                context_str += f"\n--- Page {pid} ({page_data['header']}) ---\n{page_data['content'][:500]}...\n"

            integration_prompt = f"""
            User Request: {query}

            Retrieved Pages:
            {context_str}

            Task: Synthesize the information retrieved so far into a concise summary relative to the request.
            """
            knowledge_summary = await self.llm_client.generate(integration_prompt)

        # Final Answer Generation
        final_answer_prompt = f"""
        User Request: {query}

        Final Knowledge Context:
        {knowledge_summary}

        Task: Provide a comprehensive answer to the user's request based on the researched information.
        """
        final_answer = await self.llm_client.generate(final_answer_prompt)
        return final_answer

    def _search(self, query: str, k=3) -> List[Dict]:
        results = []
        if not self.memorizer.faiss_index or self.memorizer.faiss_index.ntotal == 0:
            return []

        # Vector Search
        embedding = self.memorizer.embedding_model.encode([query])[0]
        D, I = self.memorizer.faiss_index.search(np.array([embedding], dtype=np.float32), k)

        for i, idx in enumerate(I[0]):
            if idx != -1 and idx < len(self.memorizer.page_ids_list):
                pid = self.memorizer.page_ids_list[idx]
                if pid in self.memorizer.pages:
                    page = self.memorizer.pages[pid]
                    results.append({
                        "id": pid,
                        "header": page.header,
                        "content": page.content,
                        "score": float(D[0][i])
                    })

        # Keyword Search (BM25)
        if self.memorizer.bm25:
            tokenized_query = query.lower().split()
            scores = self.memorizer.bm25.get_scores(tokenized_query)
            top_n = np.argsort(scores)[::-1][:k]

            for idx in top_n:
                if scores[idx] > 0 and idx < len(self.memorizer.page_ids_list):
                    pid = self.memorizer.page_ids_list[idx]
                    if not any(r['id'] == pid for r in results):
                         page = self.memorizer.pages[pid]
                         results.append({
                            "id": pid,
                            "header": page.header,
                            "content": page.content,
                            "score": float(scores[idx])
                        })

        return results

# --- App Setup ---

app = FastAPI(title="Archivist Service", version="1.0")
memorizer_instance: Optional[Memorizer] = None
researcher_instance: Optional[Researcher] = None

@app.on_event("startup")
async def startup():
    global memorizer_instance, researcher_instance

    llm = LLMClient(CONSUL_HOST, CONSUL_PORT, LLAMA_API_SERVICE_NAME)
    memorizer_instance = Memorizer(DB_PATH, INDEX_DIR, llm)
    researcher_instance = Researcher(memorizer_instance, llm)

    asyncio.create_task(memorizer_instance.process_loop())
    logger.info(f"Archivist started on port {PORT}")

@app.on_event("shutdown")
async def shutdown():
    if researcher_instance and researcher_instance.llm_client:
        await researcher_instance.llm_client.close()

@app.post("/research")
async def research_endpoint(req: DeepResearchRequest):
    if not researcher_instance:
        raise HTTPException(status_code=503, detail="Service initializing")

    answer = await researcher_instance.deep_research(req.query, req.max_steps)
    return {"content": answer}

@app.get("/health")
async def health_check():
    if memorizer_instance:
        return {"status": "ok", "pages_indexed": len(memorizer_instance.pages)}
    return {"status": "starting"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
