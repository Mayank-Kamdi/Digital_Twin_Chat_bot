"""Query pre-processing and hybrid RAG retriever for NovaTech Solutions."""

import re
from typing import List, Dict, Any, Optional, Tuple
from backend.rag.vector_store import VectorStore


class Retriever:
    """Pre-processes user queries and retrieves relevant knowledge chunks."""

    def __init__(self, vector_store: VectorStore, top_k: int = 4, threshold: float = 0.12):
        self.vector_store = vector_store
        self.top_k = top_k
        self.threshold = threshold

    def preprocess_query(self, query: str, context_products: Optional[List[str]] = None) -> str:
        """
        Cleans and enriches user query with recent conversational context if pronouns are present.
        """
        cleaned = re.sub(r"[^\w\s\$\-\.\?]", " ", query).strip()
        lower_q = cleaned.lower()

        # Check for pronoun / referential queries
        referential_triggers = ["it", "that", "this service", "that service", "its price", "how much is it", "tell me more about it", "what about it"]
        has_referential = any(trigger in lower_q for trigger in referential_triggers)

        if has_referential and context_products:
            # Append the most recently discussed product to the search query
            most_recent_product = context_products[-1]
            cleaned = f"{cleaned} ({most_recent_product})"

        return cleaned

    def retrieve(
        self,
        query: str,
        context_products: Optional[List[str]] = None,
        top_k: Optional[int] = None
    ) -> Tuple[List[Dict[str, Any]], float, bool]:
        """
        Retrieves relevant documents for the query.
        Returns:
            - List of retrieved documents with similarity scores
            - Max similarity score
            - In-domain flag (True if max score exceeds threshold, False if likely unknown/unrelated)
        """
        k = top_k or self.top_k
        processed_query = self.preprocess_query(query, context_products)
        raw_results = self.vector_store.search(processed_query, top_k=k)

        if not raw_results:
            return [], 0.0, False

        max_score = raw_results[0][1]

        # Entity boosting for high-priority business terms
        boosted_results = []
        lower_q = query.lower()

        for doc, score in raw_results:
            boost = 0.0
            doc_content = doc.get("content", "").lower()
            doc_title = doc.get("title", "").lower()

            # Exact phrase matches in title get boost
            if any(term in doc_title for term in ["refund", "sla", "support", "pricing", "cost", "working hours", "contact"]):
                for word in ["refund", "sla", "support", "price", "pricing", "cost", "hours", "contact"]:
                    if word in lower_q and word in doc_title:
                        boost += 0.25

            # Keyword match boosts
            if "small business" in lower_q and "small" in doc_content:
                boost += 0.20
            if "ai automation" in lower_q and "ai customer support" in doc_content:
                boost += 0.25

            final_score = min(1.0, score + boost)
            doc_copy = dict(doc)
            doc_copy["score"] = round(final_score, 4)
            boosted_results.append(doc_copy)

        # Re-sort after boosting
        boosted_results.sort(key=lambda x: x["score"], reverse=True)
        top_boosted_score = boosted_results[0]["score"] if boosted_results else 0.0

        is_in_domain = top_boosted_score >= self.threshold

        return boosted_results[:k], top_boosted_score, is_in_domain

    def format_context_for_prompt(self, documents: List[Dict[str, Any]]) -> str:
        """Formats retrieved documents into a clean context block for the LLM."""
        if not documents:
            return "No relevant business documents found in the NovaTech knowledge base."

        formatted_blocks = []
        for i, doc in enumerate(documents, start=1):
            category = doc.get("category", "General").replace("_", " ").title()
            title = doc.get("title", f"Document {i}")
            content = doc.get("content", "").strip()
            score = doc.get("score", 0.0)
            formatted_blocks.append(
                f"--- SOURCE {i} [{category}] (Relevance: {score}) ---\n"
                f"Title: {title}\n"
                f"{content}\n"
            )

        return "\n".join(formatted_blocks)
