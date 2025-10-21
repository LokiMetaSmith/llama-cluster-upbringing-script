import os
import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
#from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAG_Tool:
    """A tool to retrieve information from a project-specific knowledge base.

    This tool scans the repository for text-based documents (.md, .txt),
    chunks them, and embeds them into a searchable vector index. It allows
    the agent to find relevant information to answer user queries about the
    project.
    """
    def __init__(self, base_dir="/", model_name="all-MiniLM-L6-v2"):
        """Initializes the RAG_Tool.

        Args:
            base_dir (str): The root directory to start scanning for documents.
            model_name (str): The name of the SentenceTransformer model to use.
        """
        self.name = "rag"
        self.description = "Searches the project's documentation to answer questions."
        self.base_dir = base_dir
        self.model = SentenceTransformer(model_name)
        self.text_splitter = None
        self.documents = []
        self.index = None
        self._build_knowledge_base()

    def _build_knowledge_base(self):
        """Scans for documents, chunks them, and builds the FAISS index."""
        logging.info("Building RAG knowledge base...")
        all_chunks = []
        # Exclude irrelevant or problematic directories
        exclude_dirs = {".git", "jules-scratch", ".venv", "ansible", "docker", "e2e", "debian_service", "distributed-llama-repo"}

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
                                    # Create a simple object to mimic the previous structure
                                    chunk = type('obj', (object,), {'page_content': chunk_text, 'metadata': {"source": file_path}})
                                    all_chunks.append(chunk)
                    except Exception as e:
                        logging.warning(f"Could not read or process file {file_path}: {e}")

        if not all_chunks:
            logging.warning("No documents found for RAG tool. Knowledge base is empty.")
            return

        self.documents = all_chunks
        # We are embedding the page_content of each chunk
        embeddings = self.model.encode([doc.page_content for doc in self.documents], show_progress_bar=True)

        # Create a FAISS index
        embedding_dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(np.array(embeddings, dtype=np.float32))
        logging.info(f"RAG knowledge base built successfully with {len(self.documents)} chunks.")

    def search_knowledge_base(self, query: str) -> str:
        """Searches the knowledge base for text relevant to the query.

        Args:
            query (str): The user's question or topic to search for.

        Returns:
            str: A formatted string containing the most relevant document
                 excerpts, or a message if no relevant information is found.
        """
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
                results.append(f"From {doc.metadata['source']}:\n---\n{doc.page_content}\n---")

        if not results:
            return "I could not find any relevant information in the knowledge base to answer your question."

        return "\n\n".join(results)