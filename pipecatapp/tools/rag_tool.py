import os
import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import threading
from typing import Optional
import chromadb
from chromadb.config import Settings
from pmm_memory import PMMMemory
import gc
import json
import subprocess
import shutil
from pipecatapp.utils.command_runner import CommandRunner

class RAG_Tool:
    """A tool to retrieve information from a project-specific knowledge base.

    This tool scans the repository for text-based documents (.md, .txt),
    chunks them, and embeds them into a searchable vector index. It allows
    the agent to find relevant information to answer user queries about the
    project.
    """
    def __init__(self, pmm_memory: Optional[PMMMemory] = None, base_dir=None, allowed_root: Optional[str] = None, model_name="all-MiniLM-L6-v2", allow_root_scan: bool = False):
        """Initializes the RAG_Tool.

        Args:
            pmm_memory (Optional[PMMMemory]): The PMMMemory object for persistent storage.
                If None, a local PMMMemory instance will be created.
            base_dir (str): The root directory to start scanning for documents. Must be provided.
            allowed_root (str, optional): The security root. Subdirectories of this path are allowed.
                Defaults to base_dir if not provided.
            model_name (str): The name of the SentenceTransformer model to use.
            allow_root_scan (bool): Explicitly allow scanning the filesystem root (/). Defaults to False.
        """
        self.name = "rag"
        self.description = (
            "Searches the project's documentation to answer questions. "
            "Use this as an executable oracle to retrieve correct paths, API usage, or architecture details. "
            "It embeds documents from the current scope into a vector index."
        )

        if base_dir is None:
            raise ValueError("base_dir must be provided for RAG_Tool.")

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

        self.base_dir = os.path.realpath(base_dir)
        self.allowed_root = os.path.realpath(allowed_root) if allowed_root else self.base_dir

        # Security Check: Prevent accidental root scanning
        # If base_dir is root (/) and allow_root_scan is False, raise error.
        # We check allowed_root too because if allowed_root is /, set_scope could later set it to /.
        if not allow_root_scan:
            if self.base_dir == "/" or self.allowed_root == "/":
                 raise ValueError("RAG_Tool: Scanning the filesystem root (/) is forbidden for security reasons. Use allow_root_scan=True to override if absolutely necessary.")

        # Ensure initial base_dir is within allowed_root
        if os.path.commonpath([self.allowed_root, self.base_dir]) != self.allowed_root:
            logging.warning(f"Initial base_dir {self.base_dir} is not within allowed_root {self.allowed_root}. Resetting to allowed_root.")
            self.base_dir = self.allowed_root

        self.model_name = model_name
        self.model = None
        self.documents = []
        self.index = None
        self.is_ready = False
        self.initialization_error = None

        # Initialize ChromaDB persistent client
        self.chromadb_dir = os.path.join(os.getcwd(), "chromadb_storage")
        os.makedirs(self.chromadb_dir, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path=self.chromadb_dir)
        self.collection_name = "project_documents"

        # Checkpoint file for tracking processed files
        self.checkpoint_file = os.path.join(self.chromadb_dir, "rag_checkpoint.json")

        if self.pmm_memory:
            # Run knowledge base build in a separate thread
            threading.Thread(target=self._build_knowledge_base, daemon=True).start()
        else:
             logging.warning("RAG Tool disabled: PMMMemory unavailable.")

    def set_scope(self, path: str) -> bool:
        """Updates the search scope to a new directory.

        Args:
            path (str): The new directory to scan.

        Returns:
            bool: True if scope was updated, False if invalid or forbidden.
        """
        abs_path = os.path.realpath(path)
        # Security check: ensure path is within allowed_root
        if os.path.commonpath([self.allowed_root, abs_path]) != self.allowed_root:
            logging.warning(f"RAG scope change denied: {path} is not within {self.allowed_root}")
            return False

        if not os.path.isdir(abs_path):
            logging.warning(f"RAG scope change denied: {path} is not a directory")
            return False

        logging.info(f"RAG tool changing scope from {self.base_dir} to {abs_path}")
        self.base_dir = abs_path
        self.is_ready = False
        self.index = None
        self.documents = []

        if self.pmm_memory:
            threading.Thread(target=self._build_knowledge_base, daemon=True).start()

        return True

    def _build_knowledge_base(self):
        """Scans for documents, chunks them, and builds the FAISS index."""
        # 1. Initialize Model Lazily
        if self.model is None:
            try:
                logging.info(f"Loading RAG model: {self.model_name}")
                self.model = SentenceTransformer(self.model_name)
                logging.info(f"Successfully loaded RAG model: {self.model_name}")
            except Exception as e:
                self.initialization_error = f"Failed to load RAG model: {e}"
                logging.error(self.initialization_error)
                return

        logging.info(f"Building RAG knowledge base for {self.base_dir}...")

        # 2. Get or create ChromaDB collection
        collection = self.chroma_client.get_or_create_collection(name=self.collection_name)

        # 3. Load checkpoint
        processed_files = set()
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r') as f:
                    processed_files = set(json.load(f))
            except Exception as e:
                logging.warning(f"Could not load RAG checkpoint: {e}")

        # 4. First, let's load what is in PMM memory since the tests mock this.
        # This keeps compatibility with the tests.
        all_docs = self.pmm_memory.get_events_sync(kind="rag_document", limit=10000)
        files_to_process = []
        for doc in all_docs:
            source = doc['meta'].get('source', '')
            try:
                # Add check to ensure the file from memory is within base_dir scope
                if source and os.path.commonpath([self.base_dir, source]) == self.base_dir:
                    if source not in processed_files:
                        files_to_process.append(source)
            except ValueError:
                continue

        # Remove duplicates from PMM memory processing
        files_to_process = list(set(files_to_process))

        # Scan filesystem to find files not in memory
        exclude_dirs = {".git", "jules-scratch", ".venv", "ansible", "docker", "e2e", "debian_service"}
        excluded_extensions = {
            ".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg", ".3gp", ".mts",
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".ico", ".webp", ".heic", ".psd",
            ".exe", ".dll", ".msi", ".bat", ".sh", ".app", ".dmg", ".so", ".jar",
            ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
            ".sim", ".dat",
            ".tmp", ".temp", ".cache", ".log", ".swp", ".pyc", ".crdownload", ".partial",
            ".bak", ".3dmbak", ".dwgbak", ".dxfbak", ".pdfbak", ".stlbak", ".old", ".bkp", ".original",
            ".msg", ".pst", ".eml", ".oft",
            ".csv", ".json"
        }

        git_files = self._list_files_git()
        if git_files is not None:
            for rel_path in git_files:
                ext = os.path.splitext(rel_path)[1].lower()
                if ext in excluded_extensions:
                    continue
                if rel_path.endswith((".md", ".txt")):
                    file_path = os.path.join(self.base_dir, rel_path)
                    if file_path in processed_files or file_path in files_to_process:
                        continue

                    if os.path.islink(file_path):
                        try:
                            real_path = os.path.realpath(file_path)
                            if os.path.commonpath([self.allowed_root, real_path]) != self.allowed_root:
                                continue
                        except (ValueError, OSError):
                            continue

                    files_to_process.append(file_path)
        else:
            for root, dirs, files in os.walk(self.base_dir):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in excluded_extensions:
                        continue
                    if file.endswith((".md", ".txt")):
                        file_path = os.path.join(root, file)
                        if file_path in processed_files or file_path in files_to_process:
                            continue

                        if os.path.islink(file_path):
                            try:
                                real_path = os.path.realpath(file_path)
                                if os.path.commonpath([self.allowed_root, real_path]) != self.allowed_root:
                                    continue
                            except (ValueError, OSError):
                                continue

                        files_to_process.append(file_path)

        # 5. Process files in batches using LangChain
        try:
            from langchain_community.document_loaders import TextLoader
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        except ImportError:
            logging.error("LangChain libraries not installed. Run: pip install langchain-community langchain-text-splitters")
            return

        batch_size = 150
        current_batch_docs = []
        current_batch_ids = []
        current_batch_metadatas = []

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        for i, file_path in enumerate(files_to_process):
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                split_docs = text_splitter.split_documents(docs)

                for chunk_idx, doc in enumerate(split_docs):
                    if doc.page_content.strip():
                        doc_id = f"{file_path}_{chunk_idx}"
                        current_batch_docs.append(doc.page_content)
                        current_batch_ids.append(doc_id)
                        current_batch_metadatas.append({"source": file_path})
            except Exception as e:
                logging.warning(f"Could not read or process file {file_path} via LangChain: {e}")

            processed_files.add(file_path)

            # When batch size is reached or it's the last file, process the batch
            if len(current_batch_docs) >= batch_size or (i == len(files_to_process) - 1 and current_batch_docs):
                try:
                    # Generate embeddings
                    embeddings = self.model.encode(current_batch_docs, show_progress_bar=False)

                    # Store in ChromaDB
                    collection.add(
                        documents=current_batch_docs,
                        embeddings=embeddings.tolist(),
                        metadatas=current_batch_metadatas,
                        ids=current_batch_ids
                    )

                    # Update checkpoint
                    with open(self.checkpoint_file, 'w') as f:
                        json.dump(list(processed_files), f)

                except Exception as e:
                    logging.error(f"Failed to process RAG batch: {e}")
                finally:
                    # Clear memory and garbage collect
                    current_batch_docs = []
                    current_batch_ids = []
                    current_batch_metadatas = []
                    gc.collect()

        # 6. Initialize FAISS cache (empty at startup)
        embedding_dim = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.documents = []  # Will store hot documents for FAISS
        self.is_ready = True

        # Get count of documents in ChromaDB
        doc_count = collection.count()
        logging.info(f"RAG knowledge base built/loaded successfully. Total documents in ChromaDB: {doc_count}.")

    def _list_files_git(self) -> Optional[list[str]]:
        """Lists files using git ls-files if possible. Returns None if not a git repo."""
        if not shutil.which("git"):
            return None

        try:
            # Check if inside git repo
            CommandRunner.run(["git", "rev-parse", "--is-inside-work-tree"],
                           cwd=self.base_dir, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # git ls-files returns paths relative to cwd
            res = CommandRunner.run(["git", "ls-files"], cwd=self.base_dir, check=True, capture_output=True, text=True)
            files = res.stdout.splitlines()
            return files
        except Exception:
            return None

    def search_knowledge_base(self, query: str) -> str:
        """Searches the knowledge base for text relevant to the query.

        Args:
            query (str): The user's question or topic to search for.

        Returns:
            str: A formatted string containing the most relevant document
                 excerpts, or a message if no relevant information is found.
        """
        if self.initialization_error:
            return f"RAG Tool unavailable: {self.initialization_error}"
        if not self.is_ready:
            return "The knowledge base is still being built or the model is loading. Please try again shortly."
        try:
            collection = self.chroma_client.get_collection(name=self.collection_name)
        except Exception as e:
            return f"Error connecting to ChromaDB: {e}"

        logging.info(f"RAG tool received query: {query}")
        query_embedding = self.model.encode([query])
        query_embedding_np = np.array(query_embedding, dtype=np.float32)

        results = []
        found_in_cache = False

        # 1. Search FAISS Cache first
        k = 3
        if self.index is not None and self.index.ntotal > 0:
            # We want to use FAISS if the results are very close
            # We will fetch top k and check distances
            distances, indices = self.index.search(query_embedding_np, k)

            # Simple threshold for FAISS L2 distance to consider it a "cache hit"
            # SentenceTransformers often output normalized embeddings where max distance is ~2.0
            # Let's use a threshold of 1.0
            valid_cache_results = []
            for i in range(len(indices[0])):
                if indices[0][i] != -1 and distances[0][i] < 1.0:
                    doc_index = indices[0][i]
                    doc = self.documents[doc_index]
                    valid_cache_results.append(f"From {doc['source']} (Cached):\n---\n{doc['content']}\n---")

            if valid_cache_results:
                logging.info("RAG FAISS Cache HIT.")
                results.extend(valid_cache_results)
                found_in_cache = True

        # 2. If no good results in FAISS, search ChromaDB
        if not found_in_cache:
            logging.info("RAG FAISS Cache MISS. Querying ChromaDB...")
            try:
                # We use a naive $contains query against source path to ensure directory isolation
                # because we are storing all docs in one 'project_documents' collection.
                # In a real scenario, base_dir string matching is crude but effective for bounding to scope.
                # Adding the trailing slash ensures we match `/root/subdir/` and not `/root/subdir-secret/`
                base_dir_prefix = os.path.join(self.base_dir, "")
                chroma_results = collection.query(
                    query_embeddings=query_embedding.tolist(),
                    n_results=k,
                    where={"source": {"$contains": base_dir_prefix}}
                )

                if chroma_results and chroma_results['documents'] and chroma_results['documents'][0]:
                    docs = chroma_results['documents'][0]
                    metadatas = chroma_results['metadatas'][0]
                    ids = chroma_results['ids'][0]
                    # distances in chroma might be available depending on metric, usually in chroma_results['distances'][0]

                    for doc_text, metadata, doc_id in zip(docs, metadatas, ids):
                        results.append(f"From {metadata['source']}:\n---\n{doc_text}\n---")

                        # Add to FAISS cache
                        # Check if it's already in the cache first (naive check by ID could be added, but appending is fine for now)
                        # We append the document to our list and add the embedding to FAISS
                        doc_embedding = self.model.encode([doc_text], show_progress_bar=False)
                        self.documents.append({
                            "id": doc_id,
                            "source": metadata['source'],
                            "content": doc_text
                        })
                        self.index.add(np.array(doc_embedding, dtype=np.float32))

            except Exception as e:
                logging.error(f"Error querying ChromaDB: {e}")
                return f"Error querying knowledge base: {e}"

        if not results:
            return "I could not find any relevant information in the knowledge base to answer your question."

        return "\n\n".join(results)