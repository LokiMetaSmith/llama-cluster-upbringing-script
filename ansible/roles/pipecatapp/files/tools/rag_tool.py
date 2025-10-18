import os
import logging
import chromadb
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAG_Tool:
    """A tool to retrieve information from a project-specific knowledge base.

    This tool scans the repository for text-based documents (.md, .txt),
    chunks them, and embeds them into a dedicated 'documentation' collection
    in a central ChromaDB service.
    """
    def __init__(self, base_dir="/", chroma_host="localhost", chroma_port=8000):
        """Initializes the RAG_Tool.

        Args:
            base_dir (str): The root directory to start scanning for documents.
            chroma_host (str): The hostname of the ChromaDB service.
            chroma_port (int): The port of the ChromaDB service.
        """
        self.name = "rag"
        self.description = "Searches the project's documentation to answer questions."
        self.base_dir = base_dir
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        self.collection = self.client.get_or_create_collection(name="documentation")
        self._build_knowledge_base()

    def _build_knowledge_base(self):
        """Scans for documents, chunks them, and populates the ChromaDB collection."""
        logging.info("Building RAG knowledge base in ChromaDB...")
        # Exclude irrelevant or problematic directories
        exclude_dirs = {".git", "jules-scratch", ".venv", "ansible", "docker", "e2e", "debian_service", "distributed-llama-repo"}

        # For idempotency, we can check if the collection already has documents.
        # A more robust implementation would check file hashes to see if they need updating.
        # For now, we'll just log if the collection is already populated.
        if self.collection.count() > 0:
            logging.info("RAG knowledge base already populated. Skipping build.")
            return

        all_chunks = []
        all_metadatas = []
        all_ids = []

        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith((".md", ".txt")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        if content.strip():
                            chunks = self.text_splitter.create_documents([content])
                            for chunk in chunks:
                                all_chunks.append(chunk.page_content)
                                all_metadatas.append({"source": file_path})
                                all_ids.append(str(uuid.uuid4()))
                    except Exception as e:
                        logging.warning(f"Could not read or process file {file_path}: {e}")

        if not all_chunks:
            logging.warning("No documents found for RAG tool. Knowledge base is empty.")
            return

        # Add all documents to the collection in one batch
        self.collection.add(
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )
        logging.info(f"RAG knowledge base built successfully with {len(all_chunks)} chunks.")

    def search_knowledge_base(self, query: str) -> str:
        """Searches the knowledge base for text relevant to the query.

        Args:
            query (str): The user's question or topic to search for.

        Returns:
            str: A formatted string containing the most relevant document
                 excerpts, or a message if no relevant information is found.
        """
        if self.collection.count() == 0:
            return "The knowledge base is empty. I cannot answer questions about the project yet."

        logging.info(f"RAG tool received query: {query}")
        results = self.collection.query(
            query_texts=[query],
            n_results=3
        )

        if not results['documents'][0]:
            return "I could not find any relevant information in the knowledge base to answer your question."

        # Format the results for display
        formatted_results = []
        for i, doc in enumerate(results['documents'][0]):
            source = results['metadatas'][0][i].get('source', 'Unknown')
            formatted_results.append(f"From {source}:\n---\n{doc}\n---")

        return "\n\n".join(formatted_results)