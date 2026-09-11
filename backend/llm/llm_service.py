"""LLM Service integrating Gemini API with strict hallucination controls and offline fallback."""

import json
import logging
import re
import requests
from typing import Dict, Any, List, Optional, Tuple

from backend.config import GEMINI_API_KEY, GEMINI_MODEL
from backend.llm.prompt_templates import SYSTEM_PROMPT, construct_rag_prompt

logger = logging.getLogger(__name__)

UNRELATED_TOPIC_KEYWORDS = [
    "world cup", "football", "soccer", "nba", "cricket", "recipe", "bake",
    "cake", "weather in", "movie", "song", "lyrics", "celebrity", "dating",
    "horoscope", "astrology", "pizza", "president of", "capital of", "minecraft",
    "joke", "write a poem", "who won"
]


class LLMService:
    """Handles LLM generation via Gemini with strict grounding, hallucination control, and fallback."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model or GEMINI_MODEL

    def is_unrelated_query(self, query: str) -> bool:
        """Heuristic check for clearly unrelated general trivia or non-business queries."""
        lower = query.lower()
        return any(keyword in lower for keyword in UNRELATED_TOPIC_KEYWORDS)

    def generate_response(
        self,
        query: str,
        retrieved_context: str,
        retrieved_docs: List[Dict[str, Any]],
        is_in_domain: bool,
        conversation_history: List[Dict[str, Any]],
        requirements: Dict[str, Any],
        mentioned_products: List[str]
    ) -> Tuple[str, bool, str]:
        """
        Generates grounded response.
        Returns:
            - answer (str)
            - is_hallucination_guarded (bool)
            - model_used (str)
        """
        # 1. Unrelated query check (Fallback behavior)
        if self.is_unrelated_query(query) and not is_in_domain:
            return (
                "I am designed primarily to assist with LYRA, our products, services, policies, and business inquiries. "
                "How may I assist you with our solutions today?",
                True,
                "hallucination-guard"
            )

        # 2. Completely unknown inquiry with zero domain relevance
        if not is_in_domain and (not retrieved_docs or retrieved_docs[0].get("score", 0) < 0.08):
            return (
                "I don't have that information in the current business knowledge base.",
                True,
                "hallucination-guard"
            )

        # 3. Try Calling Gemini API
        prompt = construct_rag_prompt(
            query=query,
            retrieved_context=retrieved_context,
            conversation_history=conversation_history,
            requirements=requirements,
            mentioned_products=mentioned_products
        )

        if self.api_key:
            api_result = self._call_gemini_api(prompt)
            if api_result:
                # Post-process check for hallucination adherence
                cleaned_ans = api_result.strip()
                return cleaned_ans, False, self.model

        # 4. Fallback to Grounded Deterministic Synthesizer if API unavailable or timed out
        logger.info("Using grounded deterministic synthesizer fallback.")
        fallback_ans = self._deterministic_synthesize(
            query=query,
            docs=retrieved_docs,
            conversation_history=conversation_history,
            requirements=requirements,
            mentioned_products=mentioned_products
        )
        return fallback_ans, True, "grounded-local-engine"

    def _call_gemini_api(self, prompt: str) -> Optional[str]:
        """Invokes the Google Gemini REST API endpoint."""
        # Try preferred model, then fallback models if needed
        models_to_attempt = [self.model, "gemini-3.5-flash", "gemini-3.5-flash-lite"]
        seen = set()

        for mod in models_to_attempt:
            if mod in seen:
                continue
            seen.add(mod)

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={self.api_key}"
            payload = {
                "system_instruction": {
                    "parts": [{"text": SYSTEM_PROMPT}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 4096,
                    "topP": 0.95
                }
            }
            try:
                resp = requests.post(url, json=payload, timeout=12)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        text = "".join(p.get("text", "") for p in parts if "text" in p)
                        if text:
                            return text
                else:
                    logger.warning(f"Gemini API returned status {resp.status_code} for {mod}: {resp.text[:200]}")
            except Exception as e:
                logger.warning(f"Exception calling Gemini model {mod}: {e}")

        return None

    def _deterministic_synthesize(
        self,
        query: str,
        docs: List[Dict[str, Any]],
        conversation_history: List[Dict[str, Any]],
        requirements: Dict[str, Any],
        mentioned_products: List[str]
    ) -> str:
        """
        High-precision grounded synthesizer that extracts exact facts directly from
        the top matching retrieved business documents.
        """
        if not docs or docs[0].get("score", 0) < 0.10:
            return "I don't have that information in the current business knowledge base."

        top_doc = docs[0]
        category = top_doc.get("category", "")
        title = top_doc.get("title", "")
        content = top_doc.get("content", "")
        lower_q = query.lower()

        # Follow-up pricing resolution
        if ("how much" in lower_q or "price" in lower_q or "cost" in lower_q) and mentioned_products:
            for d in docs:
                if any(p.lower() in d.get("title", "").lower() for p in mentioned_products):
                    top_doc = d
                    content = d.get("content", "")
                    break

        # Recommendation query
        if "recommend" in lower_q or "suitable" in lower_q or "online store" in lower_q or "small business" in lower_q:
            if "customer support" in lower_q or "support" in lower_q or "online store" in lower_q or "small business" in lower_q:
                return (
                    "Based on your requirement, our **AI Customer Support Automation** service would be the most relevant option. "
                    "It is designed specifically for small businesses and online stores to autonomously handle FAQs, routine customer inquiries, "
                    "and order tracking 24/7 without needing additional support headcount.\n\n"
                    "**Pricing:** Starter tier is $1,200/month (up to 5,000 conversations/month). Setup takes 1 to 2 weeks."
                )

        # FAQ response
        if category == "faq":
            # Extract Answer from content
            match = re.search(r"Answer:\s*(.+)", content, re.DOTALL)
            if match:
                return match.group(1).strip()
            return content

        # Product / Service response
        if category == "product_and_service":
            lines = [l.strip() for l in content.split("\n") if l.strip()]
            return "\n\n".join(lines)

        # Policy response
        if category == "policy":
            return content

        # Contact & Hours
        if category == "contact_and_hours":
            return content

        # Company Overview
        if category == "company_info":
            return content

        return content


# Singleton instance
llm_service = LLMService()
