"""Session-based conversation memory and context tracker."""

import time
import re
from typing import Dict, List, Any, Optional

KNOWN_PRODUCTS = [
    "AI Customer Support Automation",
    "Enterprise RAG Knowledge System",
    "Cloud Infrastructure Optimization & DevOps",
    "Custom Workflow Automation Agent",
    "Data Analytics & BI Dashboard Suite"
]


class SessionMemory:
    """Stores conversation history and extracted business context for a single user session."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[Dict[str, Any]] = []
        self.requirements: Dict[str, Any] = {}
        self.mentioned_products: List[str] = []
        self.last_updated: float = time.time()

    def add_user_message(self, message: str) -> None:
        self.messages.append({
            "role": "user",
            "content": message,
            "timestamp": time.time()
        })
        self.last_updated = time.time()
        self._extract_entities_and_requirements(message)

    def add_assistant_message(self, message: str) -> None:
        self.messages.append({
            "role": "assistant",
            "content": message,
            "timestamp": time.time()
        })
        self.last_updated = time.time()
        self._track_mentioned_products(message)

    def _extract_entities_and_requirements(self, message: str) -> None:
        lower_msg = message.lower()

        # Extract business types
        if "online store" in lower_msg or "ecommerce" in lower_msg or "e-commerce" in lower_msg or "shopify" in lower_msg:
            self.requirements["business_type"] = "Online Store / eCommerce"
        elif "small business" in lower_msg or "startup" in lower_msg:
            self.requirements["business_type"] = "Small Business / Startup"
        elif "enterprise" in lower_msg or "large company" in lower_msg:
            self.requirements["business_type"] = "Enterprise"

        # Extract goals / needs
        needs = self.requirements.get("needs", [])
        if "automate customer support" in lower_msg or "support automation" in lower_msg or "faq" in lower_msg or "customer queries" in lower_msg:
            if "Automate customer support" not in needs:
                needs.append("Automate customer support")
        if "cloud" in lower_msg or "aws" in lower_msg or "hosting" in lower_msg or "devops" in lower_msg:
            if "Cloud optimization / DevOps" not in needs:
                needs.append("Cloud optimization / DevOps")
        if "internal search" in lower_msg or "rag" in lower_msg or "documents" in lower_msg or "knowledge base" in lower_msg:
            if "Internal document knowledge search" not in needs:
                needs.append("Internal document knowledge search")
        if "workflow" in lower_msg or "invoice" in lower_msg or "data entry" in lower_msg:
            if "Workflow automation" not in needs:
                needs.append("Workflow automation")
        if "analytics" in lower_msg or "dashboard" in lower_msg or "kpi" in lower_msg or "bi" in lower_msg:
            if "Business intelligence dashboards" not in needs:
                needs.append("Business intelligence dashboards")

        if needs:
            self.requirements["needs"] = needs

        # Track any known products mentioned by user
        self._track_mentioned_products(message)

    def _track_mentioned_products(self, message: str) -> None:
        lower_msg = message.lower()
        for prod in KNOWN_PRODUCTS:
            prod_lower = prod.lower()
            # Match full name or strong signature words
            if prod_lower in lower_msg:
                if prod not in self.mentioned_products:
                    self.mentioned_products.append(prod)
            elif "ai customer support" in lower_msg or "ai automation" in lower_msg:
                if "AI Customer Support Automation" not in self.mentioned_products:
                    self.mentioned_products.append("AI Customer Support Automation")
            elif "rag" in lower_msg or "enterprise rag" in lower_msg:
                if "Enterprise RAG Knowledge System" not in self.mentioned_products:
                    self.mentioned_products.append("Enterprise RAG Knowledge System")
            elif "cloud infrastructure" in lower_msg or "devops" in lower_msg:
                if "Cloud Infrastructure Optimization & DevOps" not in self.mentioned_products:
                    self.mentioned_products.append("Cloud Infrastructure Optimization & DevOps")
            elif "workflow automation" in lower_msg or "custom workflow" in lower_msg:
                if "Custom Workflow Automation Agent" not in self.mentioned_products:
                    self.mentioned_products.append("Custom Workflow Automation Agent")
            elif "dashboard" in lower_msg or "data analytics" in lower_msg:
                if "Data Analytics & BI Dashboard Suite" not in self.mentioned_products:
                    self.mentioned_products.append("Data Analytics & BI Dashboard Suite")

    def get_history(self, max_turns: int = 6) -> List[Dict[str, Any]]:
        """Returns recent message turns."""
        return self.messages[-(max_turns * 2):]

    def clear(self) -> None:
        self.messages.clear()
        self.requirements.clear()
        self.mentioned_products.clear()
        self.last_updated = time.time()


class ConversationMemoryManager:
    """Manages multi-session conversation memories."""

    def __init__(self):
        self.sessions: Dict[str, SessionMemory] = {}

    def get_session(self, session_id: str) -> SessionMemory:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionMemory(session_id)
        return self.sessions[session_id]

    def add_user_message(self, session_id: str, message: str) -> None:
        self.get_session(session_id).add_user_message(message)

    def add_assistant_message(self, session_id: str, message: str) -> None:
        self.get_session(session_id).add_assistant_message(message)

    def get_history(self, session_id: str, max_turns: int = 6) -> List[Dict[str, Any]]:
        return self.get_session(session_id).get_history(max_turns)

    def get_active_context(self, session_id: str) -> Dict[str, Any]:
        session = self.get_session(session_id)
        return {
            "requirements": session.requirements,
            "mentioned_products": session.mentioned_products,
            "turn_count": len(session.messages) // 2
        }

    def clear_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            self.sessions[session_id].clear()


# Singleton instance
memory_manager = ConversationMemoryManager()
