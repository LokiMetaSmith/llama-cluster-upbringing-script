import logging
import json
import re
from typing import List, Dict, Any
from pipecatapp.llm_clients import ExternalLLMClient

class RAGPruner:
    """
    A context pruner for RAG that uses a small LLM to grade retrieved chunks.
    Inspired by Kapa.ai's blog post on pruning RAG context.
    """
    def __init__(self, llm_client: ExternalLLMClient):
        self.llm_client = llm_client

    async def prune_chunks(self, query: str, chunks: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Grades each chunk on a scale of 1-5 based on its relevance to the query.

        Args:
            query: The user's question.
            chunks: A list of dictionaries containing 'id' and 'content'.

        Returns:
            A dictionary mapping chunk IDs to their numerical grade (1-5).
        """
        if not chunks:
            return {}

        prompt = self._construct_grading_prompt(query, chunks)
        response_text = await self.llm_client.process_text(prompt)

        return self._parse_grading_response(response_text, chunks)

    def _construct_grading_prompt(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        chunks_text = ""
        for chunk in chunks:
            chunks_text += f"ID: {chunk['id']}\nContent: {chunk['content']}\n\n"

        prompt = f"""
You are an expert at evaluating the relevance of documentation for answering technical questions.
Your task is to grade a set of retrieved document chunks based on how much they contribute to answering a specific question.

QUESTION: {query}

RETRIEVED CHUNKS:
{chunks_text}

Use the following 5-level scale for grading:

5: ESSENTIAL - The answer cannot be produced without this chunk, whether it answers directly or is a definition/prerequisite.
4: CONTRIBUTING - Supplies something a complete answer needs in combination with other chunks.
3: SUPPORTING - On topic and plausibly useful, but the answer is likely complete without it.
2: TANGENTIAL - Same domain or shared terminology, but no concrete contribution.
1: UNRELATED - No meaningful connection.

Analyze all chunks together as a set. Chunks that depend on each other should both receive high grades if their combination is needed.

Respond ONLY with a JSON object where the keys are the chunk IDs and the values are the numerical grades (1-5).
Example: {{"chunk_1": 5, "chunk_2": 2}}
"""
        return prompt.strip()

    def _parse_grading_response(self, response_text: str, chunks: List[Dict[str, Any]]) -> Dict[str, int]:
        try:
            # Attempt to extract JSON if the LLM added markdown or chatter
            json_match = re.search(r"(\{.*?\})", response_text, re.DOTALL)
            if json_match:
                grades = json.loads(json_match.group(1))
            else:
                grades = json.loads(response_text)

            # Ensure all IDs are present and values are valid integers
            result = {}
            for chunk in chunks:
                chunk_id = str(chunk['id'])
                # Try both original ID and string ID in case LLM converted it
                grade = grades.get(chunk_id)
                if grade is None:
                    grade = grades.get(str(chunk['id']))

                if grade is None:
                    grade = 1 # Default to 1 if missing

                try:
                    result[chunk_id] = int(grade)
                except (ValueError, TypeError):
                    result[chunk_id] = 1
            return result
        except Exception as e:
            logging.error(f"Failed to parse RAG pruner response: {e}. Response was: {response_text}")
            # Fallback: give everything a safe grade of 3 if parsing fails
            return {str(chunk['id']): 3 for chunk in chunks}
