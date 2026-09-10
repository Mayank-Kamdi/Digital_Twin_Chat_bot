# NovaTech Solutions - Business Digital Twin

A production-ready AI Digital Twin application representing **NovaTech Solutions**, an enterprise IT, cloud engineering, and AI solutions consultancy.

The application acts as an intelligent digital representative that understands NovaTech's products, services, pricing tiers, business policies, working processes, customer support channels, and FAQs. It is built with a modular RAG architecture, conversation memory, strict hallucination controls, and an admin knowledge manager.

---

## 🌟 Core Features

### 1. Minimalist & Functional Chat Interface
- Clean, responsive chat window with user and AI message bubbles.
- Real-time typing indicators.
- Quick prompt chips for common business questions.
- **Clear Chat** button to reset conversation context and memory.
- Source transparency chips showing citations from verified business documents with similarity scores.

### 2. Business Digital Twin Knowledge
Detailed business profile for **NovaTech Solutions**:
- **5 Core Products & Services**:
  1. *AI Customer Support Automation* (Starter: $1,200/mo, Pro: $2,800/mo)
  2. *Enterprise RAG Knowledge System* ($4,500 setup + $1,800/mo)
  3. *Cloud Infrastructure Optimization & DevOps* ($3,000/mo)
  4. *Custom Workflow Automation Agent* ($2,500/workflow)
  5. *Data Analytics & BI Dashboard Suite* ($2,000 setup + $800/mo)
- **5 Verified Business Policies**:
  1. 30-Day Money-Back Satisfaction Guarantee (Refund Policy)
  2. Service Level Agreement (99.9% Uptime & 2-hour critical response)
  3. Zero-Training Data Privacy Policy (SOC2 Type II & GDPR compliant)
  4. Agile Service Delivery & Milestone Code Handover Policy
  5. Subscription Cancellation Policy (30-day notice, no lock-in)
- **12+ Frequently Asked Questions (FAQs)**
- **5-Stage Working Process**: Discovery, Architecture Blueprint, Agile Sprints, QA Auditing, and Handover.
- **Customer Support & Contacts**: Support email, toll-free phone, portal, and working hours (Mon-Fri 9:00 AM – 6:00 PM EST).

### 3. RAG Pipeline & Vector Indexing
- In-memory vector database with TF-IDF and cosine similarity embeddings.
- Entity-boosted hybrid query processing.
- Dynamic runtime re-indexing when new business documents are added.

### 4. Conversation Memory & Multi-Turn Context
- Multi-turn dialogue history tracking.
- Automatic extraction of user requirements (e.g., business type, specific automation needs).
- Mentioned product resolution for follow-up questions (e.g. *"How much does that cost?"*).

### 5. Strict Hallucination Guardrails
- Answers strictly grounded in retrieved business context.
- Fallback for out-of-scope/unrelated questions: Politely redirects to NovaTech business matters.
- Fallback for unknown business questions: Responds with:
  > *"I don't have that information in the current business knowledge base."*

### 6. Admin Knowledge Manager
- Built-in admin panel allowing instant addition and vector indexing of:
  - FAQs
  - Policies
  - Products / Services
  - Custom Business Documents

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Internet connection for Gemini API calls (or runs seamlessly in offline local synthesis mode)

### 1. Launching the Application
You can run the application with a single click using `run.bat` or via terminal:

```bash
# Launch Native Desktop Window (or opens default browser)
python main.py

# Or launch as server-only
python main.py --server-only
```

Once started, open your browser at:
```
http://127.0.0.1:8000
```

### 2. Environment Variables (.env)
The project loads configurations from `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
HOST=127.0.0.1
PORT=8000
```

---

## 🧪 Running Automated Tests

The test suite covers all required functional categories:
1. Product inquiries
2. Pricing inquiries
3. FAQ inquiries
4. Policy inquiries
5. Requirement-based recommendations
6. Unknown inquiries (hallucination guard test)
7. Unrelated inquiries (polite redirect test)
8. Multi-turn context resolution
9. Dynamic admin knowledge addition & indexing
10. Conversation memory clearing

To run the test suite:
```bash
pytest tests/test_digital_twin.py -v
```

---

## 🏛️ Project Architecture

```
Nandini Twin bot/
├── .env                              # Environment variables & API key
├── main.py                           # App entry point (PyWebView Desktop + FastAPI)
├── run.bat                           # One-click Windows launch batch script
├── requirements.txt                  # Python dependencies
├── README.md                         # Documentation
├── backend/
│   ├── app.py                        # FastAPI REST routes and static server
│   ├── config.py                     # App configuration & env loader
│   ├── models.py                     # Pydantic schemas
│   ├── profile/
│   │   ├── business_profile.py       # Profile accessor & RAG chunk generator
│   │   └── data/
│   │       └── novatech_data.json    # Complete NovaTech Solutions business dataset
│   ├── rag/
│   │   ├── vector_store.py           # In-memory TF-IDF + Cosine vector DB
│   │   ├── retriever.py              # Query preprocessing & hybrid retrieval
│   │   └── knowledge_manager.py      # Vector index coordinator & runtime updates
│   ├── memory/
│   │   └── conversation_memory.py    # Session memory, requirements & entity tracking
│   └── llm/
│       ├── prompt_templates.py       # System prompt & hallucination guardrails
│       └── llm_service.py            # Gemini 3.5 Flash integration with local fallback
├── frontend/
│   ├── index.html                    # Chat interface & admin manager modal
│   ├── styles.css                    # Clean minimal styling
│   └── app.js                        # Frontend event handling & API integration
└── tests/
    └── test_digital_twin.py          # Automated verification test suite
```
