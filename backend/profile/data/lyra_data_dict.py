DEFAULT_DATA = {
    "company_info": {
        "name": "LYRA",
        "legal_name": "LYRA Inc.",
        "founded_year": 2021,
        "headquarters": "100 Innovation Boulevard, Suite 400, Boston, MA 02110, USA",
        "tagline": "Architecting Intelligent Digital Twins & AI Infrastructure for Modern Enterprises",
        "overview": "LYRA is an enterprise AI and cloud engineering consultancy that develops custom digital twins, intelligent customer support agents, and RAG knowledge systems. We bridge the gap between cutting-edge foundational models and real-world business automation, serving over 150 clients worldwide.",
        "mission": "To democratize intelligent automation and empower organizations of all sizes with reliable, hallucination-free AI twins and scalable cloud solutions.",
        "vision": "To become the global gold standard for enterprise digital twins and business-grounded artificial intelligence.",
        "business_goals": [
            "Help 500+ small-to-medium businesses automate routine operations by 2027",
            "Maintain a 99.9% uptime SLA across all client-deployed AI agent infrastructures",
            "Ensure 100% data privacy compliance (SOC2 and GDPR) with zero customer data leakage",
            "Achieve an average support ticket resolution acceleration of 75% for client operations"
        ],
        "contact": {
            "general_email": "contact@lyra.ai",
            "support_email": "support@lyra.ai",
            "sales_email": "sales@lyra.ai",
            "phone": "+1-800-555-0199",
            "international_phone": "+1-617-555-0142",
            "website": "https://www.lyra.ai",
            "working_hours": "Monday to Friday: 9:00 AM \u2013 6:00 PM EST (Emergency 24/7 on-call support available for Enterprise Tier)",
            "time_zone": "Eastern Standard Time (UTC-5)"
        },
        "departments": [
            {
                "name": "AI & Machine Learning Engineering",
                "head": "Dr. Marcus Vance",
                "focus": "Large language model fine-tuning, RAG pipelines, and digital twin architectures"
            },
            {
                "name": "Cloud Operations & DevOps",
                "head": "Sarah Jenkins",
                "focus": "Multi-cloud hosting, Kubernetes clusters, infrastructure monitoring, and security hardening"
            },
            {
                "name": "Customer Success & Support",
                "head": "David Chen",
                "focus": "Client onboarding, 24/7 ticket resolution, and post-deployment maintenance"
            },
            {
                "name": "Solutions Architecture & Enterprise Sales",
                "head": "Elena Rostova",
                "focus": "Client discovery, custom scope definition, and technological blueprints"
            },
            {
                "name": "Legal, Security & Compliance",
                "head": "Rajesh Patel",
                "focus": "SOC2, HIPAA, GDPR adherence, and ethical AI auditing"
            }
        ],
        "target_customers": [
            "Small businesses looking to automate routine customer inquiries without expanding headcount",
            "Growing eCommerce stores needing 24/7 order status and product recommendation support",
            "Mid-market SaaS enterprises needing internal RAG assistants over large documentation",
            "Professional service firms (legal, accounting, consultancy) needing secure document indexing"
        ]
    },
    "services_and_products": [
        {
            "id": "prod-001",
            "name": "AI Customer Support Automation",
            "type": "Service & Software",
            "category": "ai_agent",
            "summary": "An intelligent 24/7 omnichannel customer support digital twin that automates routine inquiries, order tracking, and FAQ resolution.",
            "best_for": "Small to medium businesses, online stores, eCommerce brands, and SaaS startups seeking to reduce response times and support overhead.",
            "pricing": {
                "starter": "$1,200/month (Includes up to 5,000 conversations/month, email & webchat integration, standard SLA)",
                "professional": "$2,800/month (Includes up to 25,000 conversations/month, omnichannel integration including WhatsApp & CRM, priority SLA)",
                "enterprise": "Custom quote starting at $5,500/month (Unlimited volume, custom fine-tuning, dedicated server hosting)"
            },
            "key_features": [
                "Natural multi-turn conversation memory",
                "Hallucination-guarded knowledge retrieval from company docs",
                "Human escalation routing when customer requests human agent",
                "Shopify, WooCommerce, Zendesk, and Freshdesk API integrations",
                "Comprehensive analytics dashboard"
            ],
            "setup_time": "1 to 2 weeks"
        },
        {
            "id": "prod-002",
            "name": "Enterprise RAG Knowledge System",
            "type": "Product & Platform",
            "category": "rag_platform",
            "summary": "A secure internal retrieval-augmented generation engine that indexes corporate PDFs, wikis, and databases for rapid staff query resolution.",
            "best_for": "Mid-to-large enterprises, law firms, healthcare institutions, and technical support teams with extensive internal documentation.",
            "pricing": {
                "setup_fee": "$4,500 one-time architecture and ingestion fee",
                "monthly_subscription": "$1,800/month (Covers vector database hosting, continuous sync, and up to 100 staff seats)",
                "additional_seats": "$15/seat/month beyond 100 users"
            },
            "key_features": [
                "Zero data leakage architecture with tenant isolation",
                "Hybrid vector and BM25 semantic retrieval engine",
                "Direct citation and page number source verification",
                "Connectors for Notion, Google Drive, Jira, Confluence, and SharePoint",
                "Role-based access control (RBAC)"
            ],
            "setup_time": "2 to 3 weeks"
        },
        {
            "id": "prod-003",
            "name": "Cloud Infrastructure Optimization & DevOps",
            "type": "Consulting & Managed Service",
            "category": "cloud_devops",
            "summary": "Full-lifecycle cloud architecture design, cost optimization, CI/CD pipeline automation, and Kubernetes cluster management on AWS, GCP, or Azure.",
            "best_for": "Businesses struggling with high cloud hosting bills, slow deployment pipelines, or scalability bottlenecks.",
            "pricing": {
                "cloud_audit": "$2,000 one-time diagnostic assessment (credited towards retained service)",
                "monthly_managed_devops": "$3,000/month (Covers up to 20 cloud servers/clusters, 99.9% uptime management)",
                "enterprise_multi_cloud": "$6,000/month (Full 24/7 SRE coverage and disaster recovery management)"
            },
            "key_features": [
                "Average 35% reduction in monthly cloud expenditure",
                "Automated zero-downtime CI/CD deployment pipelines",
                "SOC2 Type II compliance readiness audits",
                "24/7 uptime monitoring and incident response",
                "Infrastructure as Code (Terraform / Pulumi) transition"
            ],
            "setup_time": "Immediate onboarding, 30-day transformation cycle"
        },
        {
            "id": "prod-004",
            "name": "Custom Workflow Automation Agent",
            "type": "Custom Development",
            "category": "workflow_automation",
            "summary": "Bespoke autonomous software agents tailored to streamline repetitive multi-step operational tasks across CRM, ERP, accounting, and email systems.",
            "best_for": "Logistics companies, financial agencies, real estate firms, and businesses with manual data entry or reconciliation bottlenecks.",
            "pricing": {
                "per_workflow": "$2,500 per discrete automated workflow (includes discovery, design, testing, and deployment)",
                "workflow_bundle": "$9,500 package for up to 5 end-to-end operational workflows",
                "monthly_maintenance": "$400/month per workflow (covers API updates, monitoring, and error remediation)"
            },
            "key_features": [
                "Autonomous invoice parsing and payment reconciliation",
                "CRM data enrichment and auto-lead qualification",
                "Zapier, Make.com, and custom webhook API connections",
                "Self-healing error detection with email alert notifications",
                "Detailed execution audit trails"
            ],
            "setup_time": "1 to 3 weeks per workflow"
        },
        {
            "id": "prod-005",
            "name": "Data Analytics & BI Dashboard Suite",
            "type": "Platform & Service",
            "category": "bi_analytics",
            "summary": "End-to-end data pipeline construction and interactive executive business intelligence dashboards providing real-time KPI visibility.",
            "best_for": "Executive leadership, sales directors, and operations managers needing unified metrics without manual spreadsheets.",
            "pricing": {
                "setup_fee": "$2,000 one-time data warehouse & ETL pipeline setup",
                "monthly_retained_analytics": "$800/month (Includes dashboard hosting, monthly report generation, and 10 hours of custom BI requests)",
                "enterprise_bi": "$2,200/month (Real-time data streaming, unlimited custom dashboards)"
            },
            "key_features": [
                "Unified data warehouse integration (BigQuery, Snowflake, PostgreSQL)",
                "Real-time KPI tracking for revenue, churn, CAC, and operational speed",
                "Automated weekly executive performance summary emails",
                "Interactive filtering and drill-down visualizations",
                "Mobile-optimized dashboard viewing"
            ],
            "setup_time": "2 weeks"
        }
    ],
    "policies": [
        {
            "id": "pol-001",
            "title": "30-Day Money-Back Satisfaction Guarantee (Refund Policy)",
            "category": "billing_and_refunds",
            "summary": "LYRA offers a complete 30-day money-back guarantee for initial implementation and setup phases. If our solution does not meet documented milestone specifications within 30 days of kickoff, the client receives a 100% refund of setup fees.",
            "details": "Refund requests must be submitted in writing to billing@lyra.ai. Monthly retainer fees already incurred are non-refundable once services are rendered, but subscriptions can be terminated immediately without future charges."
        },
        {
            "id": "pol-002",
            "title": "Service Level Agreement (SLA) & Uptime Guarantee",
            "category": "sla_uptime",
            "summary": "We guarantee 99.9% uptime for all hosted AI digital twins, API microservices, and RAG pipelines under our active management.",
            "details": "For critical priority issues (system outage), our maximum response time is guaranteed under 2 hours. For standard inquiries, response time is under 12 hours. If uptime falls below 99.9% in a calendar month, affected clients receive a 10% credit applied toward their next billing cycle."
        },
        {
            "id": "pol-003",
            "title": "Data Privacy, Confidentiality & Model Training Policy",
            "category": "privacy_security",
            "summary": "LYRA strictly enforces a Zero-Training Policy: client proprietary data, conversation logs, and internal documents are NEVER used to train foundational AI models or shared with third parties.",
            "details": "All data in transit is encrypted with TLS 1.3, and data at rest utilizes AES-256 encryption. We comply with SOC2 Type II and GDPR standards. Clients retain 100% intellectual property rights over their data, knowledge assets, and customized twin prompts."
        },
        {
            "id": "pol-004",
            "title": "Service Delivery, Milestones & Code Handover Policy",
            "category": "delivery_handover",
            "summary": "Every development project follows a structured sprint milestone schedule with written sign-offs at each phase.",
            "details": "Upon completion of custom development and full payment, clients receive full administrative access, source code repository transfers, and comprehensive operational documentation. LYRA provides 14 days of complimentary post-handover bug fixing."
        },
        {
            "id": "pol-005",
            "title": "Subscription Cancellation & Termination Policy",
            "category": "cancellation",
            "summary": "Clients may cancel monthly managed services and subscriptions at any time with 30 days prior written notice.",
            "details": "There are no long-term lock-in contracts or early termination penalties for monthly plans. Upon termination, clients are provided with an export of all their logs, configuration files, and stored vector indices within 5 business days."
        },
        {
            "id": "pol-006",
            "title": "Enterprise Zero-Trust Data Quarantine Policy",
            "category": "security",
            "summary": "All client test data is automatically sanitized within 12 hours.",
            "details": "Under Section 4.9 of LYRA compliance, quarantined datasets are purged across all sandboxes within 12 hours."
        },
        {
            "id": "pol-007",
            "title": "Enterprise Zero-Trust Data Quarantine Policy",
            "category": "security",
            "summary": "All client test data is automatically sanitized within 12 hours.",
            "details": "Under Section 4.9 of LYRA compliance, quarantined datasets are purged across all sandboxes within 12 hours."
        },
        {
            "id": "pol-008",
            "title": "Enterprise Zero-Trust Data Quarantine Policy",
            "category": "security",
            "summary": "All client test data is automatically sanitized within 12 hours.",
            "details": "Under Section 4.9 of LYRA compliance, quarantined datasets are purged across all sandboxes within 12 hours."
        },
        {
            "id": "pol-009",
            "title": "Enterprise Zero-Trust Data Quarantine Policy",
            "category": "security",
            "summary": "All client test data is automatically sanitized within 12 hours.",
            "details": "Under Section 4.9 of LYRA compliance, quarantined datasets are purged across all sandboxes within 12 hours."
        },
        {
            "id": "pol-010",
            "title": "Enterprise Zero-Trust Data Quarantine Policy",
            "category": "security",
            "summary": "All client test data is automatically sanitized within 12 hours.",
            "details": "Under Section 4.9 of LYRA compliance, quarantined datasets are purged across all sandboxes within 12 hours."
        }
    ],
    "working_process": {
        "methodology": "5-Stage Agile Digital Twin Implementation",
        "stages": [
            {
                "step": 1,
                "name": "Discovery & Needs Assessment",
                "duration": "Days 1\u20133",
                "description": "Our solutions architects meet with your team to review existing business workflows, pain points, FAQs, documents, and target outcomes."
            },
            {
                "step": 2,
                "name": "Architecture & Blueprint Design",
                "duration": "Days 4\u20137",
                "description": "We formulate the technical architecture, choose the optimal vector indexing strategy, define hallucination guardrails, and produce a formal project blueprint."
            },
            {
                "step": 3,
                "name": "Agile Implementation Sprints",
                "duration": "Weeks 2\u20133",
                "description": "Our engineering team ingests your knowledge base, configures LLM system instructions, builds integrations (CRM, Shopify, APIs), and trains retrieval mechanisms."
            },
            {
                "step": 4,
                "name": "Quality Assurance & Hallucination Auditing",
                "duration": "Week 4",
                "description": "Rigorous stress testing across edge cases, out-of-scope prompts, jailbreak defense, and recommendation accuracy with client stakeholders."
            },
            {
                "step": 5,
                "name": "Deployment, Handover & Staff Training",
                "duration": "Final Handover",
                "description": "Production launch, integration into client channels, delivery of admin documentation, and training sessions for client support staff."
            }
        ]
    },
    "customer_support": {
        "channels": [
            "Online Web Chat & Digital Twin (Instant 24/7)",
            "Email: support@lyra.ai (Mon-Fri 9AM-6PM EST, < 4h response)",
            "Direct Phone: +1-800-555-0199 (Toll-free, Mon-Fri 9AM-6PM EST)",
            "Client Support Portal: https://portal.lyra.ai"
        ],
        "support_hours": "Monday through Friday, 9:00 AM \u2013 6:00 PM Eastern Standard Time (EST). Enterprise clients have 24/7 emergency hotline access.",
        "ticket_tiers": [
            {
                "level": "Tier 1",
                "description": "Routine inquiries, configuration changes, user guidance. Addressed within 4 business hours."
            },
            {
                "level": "Tier 2",
                "description": "Integration glitches, prompt tuning, API errors. Addressed within 2 business hours."
            },
            {
                "level": "Tier 3 (Critical)",
                "description": "System outages, down services. Addressed within 30 minutes 24/7."
            }
        ]
    },
    "faqs": [
        {
            "id": "faq-001",
            "question": "What services does LYRA provide?",
            "answer": "LYRA provides five core services: 1) AI Customer Support Automation (intelligent 24/7 customer service twins), 2) Enterprise RAG Knowledge Systems (secure internal search over company documents), 3) Cloud Infrastructure Optimization & DevOps (cost reduction and CI/CD pipelines), 4) Custom Workflow Automation Agents (operational automation across CRM/ERP), and 5) Data Analytics & BI Dashboard Suites (real-time executive reporting)."
        },
        {
            "id": "faq-002",
            "question": "What is the price of your AI automation service?",
            "answer": "Our AI Customer Support Automation starts at $1,200/month for the Starter tier (up to 5,000 conversations/month), $2,800/month for the Professional tier (up to 25,000 conversations/month with omnichannel support), and custom enterprise tiers starting at $5,500/month for unlimited conversations and custom fine-tuning."
        },
        {
            "id": "faq-003",
            "question": "Which service is suitable for a small business?",
            "answer": "For small businesses, our AI Customer Support Automation (Starter tier at $1,200/month) is the most popular choice as it resolves repetitive customer inquiries and FAQs 24/7 without needing to hire additional staff. For businesses looking to automate specific manual tasks like invoicing or CRM updates, our Custom Workflow Automation Agent ($2,500/workflow) is also highly suitable."
        },
        {
            "id": "faq-004",
            "question": "What is your refund policy?",
            "answer": "LYRA offers a 30-day money-back satisfaction guarantee on all initial implementation and setup phases. If our solution does not achieve the agreed milestone deliverables within 30 days of project kickoff, you will receive a 100% refund of your setup fees."
        },
        {
            "id": "faq-005",
            "question": "How can I contact customer support?",
            "answer": "You can contact LYRA customer support via email at support@lyra.ai, by phone at +1-800-555-0199 (Mon\u2013Fri 9:00 AM \u2013 6:00 PM EST), or via our online client portal at portal.lyra.ai. Enterprise tier clients also have access to our 24/7 emergency support line."
        },
        {
            "id": "faq-006",
            "question": "Explain your AI automation service.",
            "answer": "Our AI Customer Support Automation is an end-to-end digital twin system. It connects directly to your company's product catalogs, knowledge base, policies, and CRM (e.g. Zendesk, Shopify). It autonomously answers customer questions, tracks orders, solves routine issues, and intelligently escalates complex inquiries to human agents when needed, operating 24/7 with zero hallucinations."
        },
        {
            "id": "faq-007",
            "question": "Can you recommend a service based on my requirements?",
            "answer": "Yes, absolutely! If you describe your business situation, current bottlenecks, or goals (for instance, high support volume, unorganized documents, high cloud costs, or manual data entry), I will analyze your requirements and recommend the exact LYRA solution tailored to your operational needs."
        },
        {
            "id": "faq-008",
            "question": "What products does the company offer?",
            "answer": "LYRA offers five principal products and services: 1) AI Customer Support Automation, 2) Enterprise RAG Knowledge System, 3) Cloud Infrastructure Optimization & DevOps, 4) Custom Workflow Automation Agent, and 5) Data Analytics & BI Dashboard Suite."
        },
        {
            "id": "faq-009",
            "question": "What are the company's working hours?",
            "answer": "LYRA business and customer support hours are Monday through Friday, 9:00 AM to 6:00 PM Eastern Standard Time (EST). Emergency support for enterprise SLA clients is available 24/7."
        },
        {
            "id": "faq-010",
            "question": "Tell me about the company.",
            "answer": "LYRA Inc. was founded in 2021 and is headquartered in Boston, MA. We specialize in building reliable, grounded AI digital twins, enterprise RAG knowledge engines, and modern cloud infrastructure. Our mission is to democratize intelligent automation for businesses of all sizes, with a strict emphasis on zero hallucinations, data privacy, and measurable ROI."
        },
        {
            "id": "faq-011",
            "question": "How long does implementation typically take?",
            "answer": "Most of our implementations take between 1 to 3 weeks. AI Customer Support Automation takes 1\u20132 weeks, Custom Workflow Automation takes 1\u20133 weeks, and full Enterprise RAG Knowledge Systems take 2\u20133 weeks from kickoff to production deployment."
        },
        {
            "id": "faq-012",
            "question": "Is my company's data safe and private?",
            "answer": "Yes. We operate under a strict Zero-Training Policy: your proprietary company data and customer communications are never used to train external models. All data is encrypted in transit (TLS 1.3) and at rest (AES-256), and our infrastructure is SOC2 Type II and GDPR compliant."
        }
    ]
}