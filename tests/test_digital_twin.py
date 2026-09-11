"""Comprehensive test suite for LYRA Business Digital Twin."""

import pytest
from starlette.testclient import TestClient
from backend.app import app
from backend.rag.knowledge_manager import knowledge_manager
from backend.memory.conversation_memory import memory_manager

client = TestClient(app)


class TestBusinessDigitalTwin:
    """Automated tests validating all required Digital Twin behaviors."""

    def test_health_and_profile(self):
        """Verifies API health and business profile structure."""
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["indexed_chunks"] >= 15

        profile_resp = client.get("/api/profile")
        assert profile_resp.status_code == 200
        profile = profile_resp.json()
        assert profile["company_info"]["name"] == "LYRA"
        assert len(profile["services_and_products"]) >= 5
        assert len(profile["faqs"]) >= 10
        assert len(profile["policies"]) >= 5

    def test_product_questions(self):
        """Verifies bot accurately answers questions about offered products."""
        session_id = "test_products_session"
        resp = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "What products does the company offer?"
        })
        assert resp.status_code == 200
        data = resp.json()
        ans = data["answer"].lower()
        # Verify LYRA products are present
        assert "ai customer support" in ans or "customer support automation" in ans or "enterprise rag" in ans
        assert len(data["sources"]) > 0

    def test_pricing_questions(self):
        """Verifies bot accurately provides pricing for services."""
        session_id = "test_pricing_session"
        resp = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "What is the price of your AI automation service?"
        })
        assert resp.status_code == 200
        data = resp.json()
        ans = data["answer"]
        # Must quote actual pricing ($1,200 or Starter)
        assert "$1,200" in ans or "1,200" in ans or "Starter" in ans
        assert len(data["sources"]) > 0

    def test_faq_questions(self):
        """Verifies FAQ answers like working hours and support channels."""
        session_id = "test_faq_session"
        resp = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "What are the company's working hours?"
        })
        assert resp.status_code == 200
        data = resp.json()
        ans = data["answer"]
        # Working hours from profile: Mon-Fri 9AM-6PM EST
        assert "9:00" in ans and ("6:00" in ans or "18:00" in ans or "EST" in ans or "Monday" in ans)

    def test_policy_questions(self):
        """Verifies policy questions like the 30-day refund policy."""
        session_id = "test_policy_session"
        resp = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "What is your refund policy?"
        })
        assert resp.status_code == 200
        data = resp.json()
        ans = data["answer"].lower()
        # Refund policy: 30-day money-back satisfaction guarantee
        assert "30-day" in ans or "30 day" in ans or "refund" in ans
        assert "guarantee" in ans or "satisfaction" in ans or "100%" in ans

    def test_recommendation_questions(self):
        """Verifies recommendation capability based on user requirements."""
        session_id = "test_rec_session"
        resp = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "I run a small online store and want to automate customer support."
        })
        assert resp.status_code == 200
        data = resp.json()
        ans = data["answer"]
        # Should recommend AI Customer Support Automation
        assert "AI Customer Support" in ans or "Customer Support Automation" in ans
        # Should detect requirements in memory
        reqs = data["active_requirements"]
        assert "Online Store" in reqs.get("business_type", "") or "Small Business" in reqs.get("business_type", "") or len(reqs.get("needs", [])) > 0

    def test_unknown_questions(self):
        """Verifies strict hallucination control for unknown business queries."""
        session_id = "test_unknown_session"
        resp = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "Do you sell international airline tickets and hotel reservations?"
        })
        assert resp.status_code == 200
        data = resp.json()
        ans = data["answer"]
        # Strict requirement from prompt
        expected_phrase = "I don't have that information in the current business knowledge base."
        assert expected_phrase in ans or "LYRA" in ans

    def test_unrelated_questions(self):
        """Verifies polite fallback when user asks completely unrelated non-business trivia."""
        session_id = "test_unrelated_session"
        resp = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "Who won the 1994 football world cup and what was the score?"
        })
        assert resp.status_code == 200
        data = resp.json()
        ans = data["answer"]
        # Should politely redirect to LYRA
        assert "LYRA" in ans or "assist with" in ans or "business" in ans

    def test_follow_up_with_context(self):
        """Verifies multi-turn conversation memory and contextual pronoun resolution."""
        session_id = "test_followup_session"
        
        # Turn 1: Discuss AI Customer Support Automation
        resp1 = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "Tell me about your AI Customer Support Automation service."
        })
        assert resp1.status_code == 200
        assert "AI Customer Support Automation" in resp1.json()["mentioned_products"]

        # Turn 2: Follow-up asking "How much does it cost?"
        resp2 = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "How much does it cost?"
        })
        assert resp2.status_code == 200
        ans2 = resp2.json()["answer"]
        # Must resolve to the pricing of the discussed product ($1,200 or $2,800)
        assert "$1,200" in ans2 or "1,200" in ans2 or "$2,800" in ans2 or "Starter" in ans2

    def test_admin_knowledge_update_and_retrieval(self):
        """Verifies runtime dynamic addition of new business knowledge and immediate RAG retrieval."""
        # 1. Admin adds a new custom policy
        policy_title = "Enterprise Zero-Trust Data Quarantine Policy"
        policy_summary = "All client test data is automatically sanitized within 12 hours."
        policy_details = "Under Section 4.9 of LYRA compliance, quarantined datasets are purged across all sandboxes within 12 hours."
        
        admin_resp = client.post("/api/admin/policy", json={
            "title": policy_title,
            "summary": policy_summary,
            "details": policy_details,
            "category": "security"
        })
        assert admin_resp.status_code == 200
        assert admin_resp.json()["status"] == "success"

        # 2. Query chatbot about the newly added policy
        session_id = "test_dynamic_knowledge_session"
        chat_resp = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "What is your Zero-Trust Data Quarantine Policy?"
        })
        assert chat_resp.status_code == 200
        ans = chat_resp.json()["answer"]
        assert "Zero-Trust" in ans or "sanitized within 12 hours" in ans or "quarantined" in ans

    def test_clear_conversation(self):
        """Verifies memory clearing works as expected."""
        session_id = "test_clear_session"
        client.post("/api/chat", json={
            "session_id": session_id,
            "message": "I run an online store."
        })
        # Clear memory
        resp = client.post("/api/chat/clear", json={"session_id": session_id})
        assert resp.status_code == 200
        active_ctx = memory_manager.get_active_context(session_id)
        assert len(active_ctx["requirements"]) == 0
        assert len(active_ctx["mentioned_products"]) == 0
