import os
import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import threading
from typing import Optional
from pmm_memory import PMMMemory

class RAG_Tool:
    """A tool to retrieve information from a project-specific knowledge base.

    This tool scans the repository for text-based documents (.md, .txt),
    chunks them, and embeds them into a searchable vector index. It allows
    the agent to find relevant information to answer user queries about the
    project.
    """
    def __init__(self, pmm_memory: Optional[PMMMemory] = None, base_dir="/", model_name="all-MiniLM-L6-v2"):
        """Initializes the RAG_Tool.

        Args:
            pmm_memory (Optional[PMMMemory]): The PMMMemory object for persistent storage.
                If None, a local PMMMemory instance will be created.
            base_dir (str): The root directory to start scanning for documents.
            model_name (str): The name of the SentenceTransformer model to use.
        """
        self.name = "rag"
        self.description = "Searches the project's documentation to answer questions."

        if pmm_memory:
            self.pmm_memory = pmm_memory
        else:
            # Import here to avoid circular dependencies if this is used elsewhere
            try:
                from pmm_memory import PMMMemory as LocalPMMMemory
                # Use a local database file for standalone operation
                self.pmm_memory = LocalPMMMemory(db_path="rag_knowledge_base.db")
            except ImportError:
                logging.error("Could not import PMMMemory. RAG tool will not function.")
                self.pmm_memory = None

        self.base_dir = base_dir
        self.model = SentenceTransformer(model_name)
        self.documents = []
        self.index = None
        self.is_ready = False

        if self.pmm_memory:
            # Run knowledge base build in a separate thread
            threading.Thread(target=self._build_knowledge_base, daemon=True).start()
        else:
             logging.warning("RAG Tool disabled: PMMMemory unavailable.")

    def _build_knowledge_base(self):
        """Scans for documents, chunks them, and builds the FAISS index."""
        logging.info("Building RAG knowledge base...")

        # Load existing documents from PMM memory to avoid reprocessing
        self.documents = self.pmm_memory.get_events(kind="rag_document", limit=10000) # Arbitrary high limit

        if not self.documents:
            logging.info("No existing RAG documents found in memory, scanning filesystem...")
            all_chunks = []
            # Exclude irrelevant or problematic directories
            exclude_dirs = {".git", "jules-scratch", ".venv", "ansible", "docker", "e2e", "debian_service"}

            for root, dirs, files in os.walk(self.base_dir):
                # Modify the list of directories in-place to prune the search
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

                for file in files:
                    if file.endswith((".md", ".txt")):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()

                            if content.strip(): # Ensure file is not empty
                                # Simple split by paragraph
                                chunks = content.split("\n\n")
                                for chunk_text in chunks:
                                    if chunk_text.strip():
                                        self.pmm_memory.add_event(
                                            kind="rag_document",
                                            content=chunk_text,
                                            meta={"source": file_path}
                                        )
                        except Exception as e:
                            logging.warning(f"Could not read or process file {file_path}: {e}")

            self.documents = self.pmm_memory.get_events(kind="rag_document", limit=10000)

        if not self.documents:
            logging.warning("No documents found for RAG tool. Knowledge base is empty.")
            self.is_ready = True
            return

        # We are embedding the page_content of each chunk
        embeddings = self.model.encode([doc['content'] for doc in self.documents], show_progress_bar=True)

        # Create a FAISS index
        embedding_dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.is_ready = True
        logging.info(f"RAG knowledge base built successfully with {len(self.documents)} chunks.")

    def search_knowledge_base(self, query: str) -> str:
        """Searches the knowledge base for text relevant to the query.

        Args:
            query (str): The user's question or topic to search for.

        Returns:
            str: A formatted string containing the most relevant document
                 excerpts, or a message if no relevant information is found.
        """
        if not self.is_ready:
            return "The knowledge base is still being built. Please try again shortly."
        if self.index is None or not self.documents:
            return "The knowledge base is empty. I cannot answer questions about the project yet."

        logging.info(f"RAG tool received query: {query}")
        query_embedding = self.model.encode([query])

        # Search the index for the top 3 most similar chunks
        k = 3
        distances, indices = self.index.search(np.array(query_embedding, dtype=np.float32), k)

        results = []
        for i in range(len(indices[0])):
            if indices[0][i] != -1: # FAISS returns -1 for no result
                doc_index = indices[0][i]
                doc = self.documents[doc_index]
                results.append(f"From {doc['meta']['source']}:\n---\n{doc['content']}\n---")

        if not results:
            return "I could not find any relevant information in the knowledge base to answer your question."

        return "\n\n".join(results)