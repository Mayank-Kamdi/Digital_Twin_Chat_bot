"""Knowledge manager coordinating business profile, vector store, and updates."""

from typing import List, Dict, Any, Optional
from backend.profile.business_profile import BusinessProfile, novatech_profile
from backend.rag.vector_store import VectorStore
from backend.rag.retriever import Retriever
from backend.config import TOP_K_CHUNKS, SIMILARITY_THRESHOLD


class KnowledgeManager:
    """Coordinates business knowledge base indexing, updates, and vector retrieval."""

    def __init__(self, profile: Optional[BusinessProfile] = None):
        self.profile = profile or novatech_profile
        self.vector_store = VectorStore()
        self.retriever = Retriever(
            vector_store=self.vector_store,
            top_k=TOP_K_CHUNKS,
            threshold=SIMILARITY_THRESHOLD
        )
        self.initialize_index()

    def initialize_index(self) -> None:
        """Loads all initial documents from the business profile into the vector store."""
        docs = self.profile.to_rag_documents()
        self.vector_store.add_documents(docs)

    def retrieve(self, query: str, context_products: Optional[List[str]] = None):
        return self.retriever.retrieve(query, context_products)

    def format_context_for_prompt(self, documents: List[Dict[str, Any]]) -> str:
        return self.retriever.format_context_for_prompt(documents)

    def add_custom_document(self, title: str, content: str, category: str = "custom_document") -> Dict[str, Any]:
        """Adds a custom document and updates vector index immediately."""
        doc_id = f"doc-custom-{len(self.vector_store.documents) + 1:03d}"
        new_doc = {
            "id": doc_id,
            "category": category,
            "title": title,
            "content": content,
            "metadata": {"type": "custom", "custom_title": title}
        }
        self.vector_store.add_document(new_doc)
        return new_doc

    def add_faq(self, question: str, answer: str) -> Dict[str, Any]:
        """Adds a new FAQ to profile and vector index."""
        new_faq = self.profile.add_faq(question, answer)
        new_doc = {
            "id": f"doc-{new_faq['id']}",
            "category": "faq",
            "title": f"FAQ: {question}",
            "content": f"Question: {question}\nAnswer: {answer}",
            "metadata": {"type": "faq", "faq_id": new_faq["id"]}
        }
        self.vector_store.add_document(new_doc)
        return new_faq

    def add_policy(self, title: str, summary: str, details: str, category: str = "general") -> Dict[str, Any]:
        """Adds a new policy to profile and vector index."""
        new_policy = self.profile.add_policy(title, summary, details, category)
        new_doc = {
            "id": f"doc-{new_policy['id']}",
            "category": "policy",
            "title": f"Policy: {title}",
            "content": (
                f"Policy Title: {title}\n"
                f"Policy Category: {category}\n"
                f"Summary: {summary}\n"
                f"Policy Details: {details}"
            ),
            "metadata": {"type": "policy", "policy_id": new_policy["id"]}
        }
        self.vector_store.add_document(new_doc)
        return new_policy

    def add_product(self, name: str, category: str, summary: str, best_for: str, pricing: Dict[str, str], features: List[str]) -> Dict[str, Any]:
        """Adds a new product/service to profile and vector index."""
        new_prod = self.profile.add_product_or_service(name, category, summary, best_for, pricing, features)
        pricing_info = "\n".join([f"  * {tier}: {price}" for tier, price in pricing.items()])
        features_info = "\n".join([f"  * {feat}" for feat in features])
        new_doc = {
            "id": f"doc-{new_prod['id']}",
            "category": "product_and_service",
            "title": f"Service/Product: {name}",
            "content": (
                f"Product/Service Name: {name}\n"
                f"Type: Service & Software | Category: {category}\n"
                f"Summary: {summary}\n"
                f"Best For / Suitable For: {best_for}\n"
                f"Pricing Structure:\n{pricing_info}\n"
                f"Key Features:\n{features_info}\n"
                f"Typical Setup Time: 1 to 2 weeks"
            ),
            "metadata": {"type": "service", "product_id": new_prod["id"], "product_name": name}
        }
        self.vector_store.add_document(new_doc)
        return new_prod

    def list_knowledge_items(self) -> List[Dict[str, Any]]:
        return self.vector_store.get_all_documents()


# Singleton instance
knowledge_manager = KnowledgeManager()
