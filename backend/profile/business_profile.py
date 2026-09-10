"""Business Profile manager for NovaTech Solutions."""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

DATA_PATH = Path(__file__).parent / "data" / "novatech_data.json"


class BusinessProfile:
    """Encapsulates the structured profile and knowledge of NovaTech Solutions."""

    def __init__(self, data_file: Optional[Path] = None):
        self.data_file = data_file or DATA_PATH
        self._data: Dict[str, Any] = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        if not self.data_file.exists():
            raise FileNotFoundError(f"Business profile data not found at {self.data_file}")
        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self) -> None:
        """Persists current data back to file."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    @property
    def company_info(self) -> Dict[str, Any]:
        return self._data.get("company_info", {})

    @property
    def services_and_products(self) -> List[Dict[str, Any]]:
        return self._data.get("services_and_products", [])

    @property
    def policies(self) -> List[Dict[str, Any]]:
        return self._data.get("policies", [])

    @property
    def working_process(self) -> Dict[str, Any]:
        return self._data.get("working_process", {})

    @property
    def customer_support(self) -> Dict[str, Any]:
        return self._data.get("customer_support", {})

    @property
    def faqs(self) -> List[Dict[str, Any]]:
        return self._data.get("faqs", [])

    def get_full_profile(self) -> Dict[str, Any]:
        """Returns complete structured business profile."""
        return self._data

    def get_company_overview_summary(self) -> str:
        ci = self.company_info
        return (
            f"{ci.get('name')} ({ci.get('legal_name')}), founded in {ci.get('founded_year')}. "
            f"Headquartered at {ci.get('headquarters')}. "
            f"Tagline: {ci.get('tagline')}. "
            f"Overview: {ci.get('overview')} "
            f"Mission: {ci.get('mission')} "
            f"Vision: {ci.get('vision')}"
        )

    def to_rag_documents(self) -> List[Dict[str, Any]]:
        """Converts the business profile into structured, searchable RAG documents with metadata."""
        docs = []

        # 1. Company Overview & Goals
        ci = self.company_info
        docs.append({
            "id": "doc-company-overview",
            "category": "company_info",
            "title": "Company Overview & Mission",
            "content": (
                f"Company: {ci.get('name')}\n"
                f"Headquarters: {ci.get('headquarters')}\n"
                f"Founded: {ci.get('founded_year')}\n"
                f"Overview: {ci.get('overview')}\n"
                f"Mission: {ci.get('mission')}\n"
                f"Vision: {ci.get('vision')}\n"
                f"Business Goals: {', '.join(ci.get('business_goals', []))}\n"
                f"Target Customers: {', '.join(ci.get('target_customers', []))}"
            ),
            "metadata": {"type": "overview", "entity": "NovaTech Solutions"}
        })

        # 2. Contact Information & Hours
        contact = ci.get("contact", {})
        docs.append({
            "id": "doc-company-contact",
            "category": "contact_and_hours",
            "title": "Contact Information & Business Working Hours",
            "content": (
                f"NovaTech Solutions Contact Details:\n"
                f"General Email: {contact.get('general_email')}\n"
                f"Support Email: {contact.get('support_email')}\n"
                f"Sales Email: {contact.get('sales_email')}\n"
                f"Toll-Free Phone: {contact.get('phone')}\n"
                f"International Phone: {contact.get('international_phone')}\n"
                f"Website: {contact.get('website')}\n"
                f"Working Hours: {contact.get('working_hours')}\n"
                f"Time Zone: {contact.get('time_zone')}"
            ),
            "metadata": {"type": "contact", "entity": "NovaTech Solutions"}
        })

        # 3. Departments & Organization
        depts = ci.get("departments", [])
        dept_lines = [f"- {d['name']} (Led by {d['head']}): {d['focus']}" for d in depts]
        docs.append({
            "id": "doc-company-departments",
            "category": "departments",
            "title": "Organizational Structure & Departments",
            "content": "NovaTech Solutions Organizational Structure & Departments:\n" + "\n".join(dept_lines),
            "metadata": {"type": "departments", "entity": "NovaTech Solutions"}
        })

        # 4. Products & Services (individual chunk per product for maximum precision)
        for prod in self.services_and_products:
            pricing_info = "\n".join([f"  * {tier}: {price}" for tier, price in prod.get("pricing", {}).items()])
            features_info = "\n".join([f"  * {feat}" for feat in prod.get("key_features", [])])
            docs.append({
                "id": f"doc-{prod['id']}",
                "category": "product_and_service",
                "title": f"Service/Product: {prod['name']}",
                "content": (
                    f"Product/Service Name: {prod['name']}\n"
                    f"Type: {prod['type']} | Category: {prod['category']}\n"
                    f"Summary: {prod['summary']}\n"
                    f"Best For / Suitable For: {prod['best_for']}\n"
                    f"Pricing Structure:\n{pricing_info}\n"
                    f"Key Features:\n{features_info}\n"
                    f"Typical Setup Time: {prod['setup_time']}"
                ),
                "metadata": {
                    "type": "service",
                    "product_id": prod["id"],
                    "product_name": prod["name"],
                    "category": prod["category"]
                }
            })

        # 5. Policies
        for pol in self.policies:
            docs.append({
                "id": f"doc-{pol['id']}",
                "category": "policy",
                "title": f"Policy: {pol['title']}",
                "content": (
                    f"Policy Title: {pol['title']}\n"
                    f"Policy Category: {pol['category']}\n"
                    f"Summary: {pol['summary']}\n"
                    f"Policy Details: {pol['details']}"
                ),
                "metadata": {"type": "policy", "policy_id": pol["id"]}
            })

        # 6. Working Process
        wp = self.working_process
        stages_info = "\n".join([
            f"Stage {s['step']}: {s['name']} ({s['duration']}) - {s['description']}"
            for s in wp.get("stages", [])
        ])
        docs.append({
            "id": "doc-working-process",
            "category": "working_process",
            "title": f"Working Process: {wp.get('methodology')}",
            "content": f"NovaTech Solutions Methodology: {wp.get('methodology')}\n\nStages:\n{stages_info}",
            "metadata": {"type": "process"}
        })

        # 7. Customer Support Information
        cs = self.customer_support
        channels_info = "\n".join([f"- {c}" for c in cs.get("channels", [])])
        tiers_info = "\n".join([f"- {t['level']}: {t['description']}" for t in cs.get("ticket_tiers", [])])
        docs.append({
            "id": "doc-customer-support",
            "category": "customer_support",
            "title": "Customer Support Channels & Ticket Resolution Tiers",
            "content": (
                f"Customer Support Information:\n"
                f"Support Hours: {cs.get('support_hours')}\n"
                f"Support Channels:\n{channels_info}\n"
                f"Support Ticket Tiers & Response Guarantees:\n{tiers_info}"
            ),
            "metadata": {"type": "support"}
        })

        # 8. FAQs
        for faq in self.faqs:
            docs.append({
                "id": f"doc-{faq['id']}",
                "category": "faq",
                "title": f"FAQ: {faq['question']}",
                "content": f"Question: {faq['question']}\nAnswer: {faq['answer']}",
                "metadata": {"type": "faq", "faq_id": faq["id"]}
            })

        return docs

    def add_faq(self, question: str, answer: str) -> Dict[str, Any]:
        """Admin helper: adds a new FAQ to the profile."""
        faq_id = f"faq-{len(self.faqs) + 1:03d}"
        new_faq = {"id": faq_id, "question": question, "answer": answer}
        self._data["faqs"].append(new_faq)
        self.save_data()
        return new_faq

    def add_policy(self, title: str, summary: str, details: str, category: str = "general") -> Dict[str, Any]:
        """Admin helper: adds a new policy to the profile."""
        pol_id = f"pol-{len(self.policies) + 1:03d}"
        new_policy = {"id": pol_id, "title": title, "category": category, "summary": summary, "details": details}
        self._data["policies"].append(new_policy)
        self.save_data()
        return new_policy

    def add_product_or_service(self, name: str, category: str, summary: str, best_for: str, pricing: Dict[str, str], features: List[str]) -> Dict[str, Any]:
        """Admin helper: adds a new product or service."""
        prod_id = f"prod-{len(self.services_and_products) + 1:03d}"
        new_prod = {
            "id": prod_id,
            "name": name,
            "type": "Service & Software",
            "category": category,
            "summary": summary,
            "best_for": best_for,
            "pricing": pricing,
            "key_features": features,
            "setup_time": "1 to 2 weeks"
        }
        self._data["services_and_products"].append(new_prod)
        self.save_data()
        return new_prod


# Singleton instance
novatech_profile = BusinessProfile()
