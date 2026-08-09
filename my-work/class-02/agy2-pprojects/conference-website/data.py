"""
Data model and dummy dataset for CloudCon 2026: Google Cloud Innovations Conference.
Contains event metadata, speakers, 8 technical talks, categories, and schedule timetable.
"""

EVENT_INFO = {
    "title": "CloudCon 2026: Google Cloud Innovations",
    "tagline": "Empowering Enterprise Applications with AI, Kubernetes, Serverless & Data at Scale",
    "date": "Thursday, October 15, 2026",
    "location": "Google Developer Center & Virtual Stream",
    "address": "345 Spear Street, San Francisco, CA 94105",
    "timezone": "PST (UTC-8)",
    "description": "Join leading cloud architects, developers, and AI researchers for a 1-day deep dive into Google Cloud Platform technologies. Experience 8 expert-led sessions, live technical demos, and high-impact networking.",
    "stats": {
        "talks": 8,
        "speakers": 10,
        "lunch_break_mins": 60,
        "tracks": 2
    }
}

CATEGORIES = [
    {"id": "ai_ml", "name": "AI & Machine Learning", "badge_class": "badge-ai"},
    {"id": "containers", "name": "Containers & Serverless", "badge_class": "badge-containers"},
    {"id": "data_analytics", "name": "Data & Analytics", "badge_class": "badge-data"},
    {"id": "security", "name": "Security & Governance", "badge_class": "badge-security"},
    {"id": "architecture", "name": "Architecture & Operations", "badge_class": "badge-arch"}
]

SPEAKERS = {
    1: {
        "id": 1,
        "first_name": "Maya",
        "last_name": "Lin",
        "role": "Principal AI Researcher",
        "company": "Google Cloud AI",
        "linkedin_url": "https://www.linkedin.com/in/maya-lin-gcp-ai",
        "avatar_initials": "ML",
        "bio": "Specializes in foundation models, Gemini fine-tuning, and scalable enterprise Generative AI architectures."
    },
    2: {
        "id": 2,
        "first_name": "Carlos",
        "last_name": "Mendoza",
        "role": "Staff Cloud Solutions Architect",
        "company": "Google Cloud",
        "linkedin_url": "https://www.linkedin.com/in/carlos-mendoza-cloud",
        "avatar_initials": "CM",
        "bio": "12+ years experience building large-scale distributed systems and Vertex AI pipeline automation."
    },
    3: {
        "id": 3,
        "first_name": "Sarah",
        "last_name": "Jenkins",
        "role": "Lead Kubernetes Specialist",
        "company": "CloudNative Labs",
        "linkedin_url": "https://www.linkedin.com/in/sarah-jenkins-k8s",
        "avatar_initials": "SJ",
        "bio": "CNCF contributor focused on GKE Autopilot, multi-cluster service mesh, and cost-efficient pod autoscaling."
    },
    4: {
        "id": 4,
        "first_name": "David",
        "last_name": "Kowalski",
        "role": "Director of Security Architecture",
        "company": "CyberShield Tech",
        "linkedin_url": "https://www.linkedin.com/in/david-kowalski-sec",
        "avatar_initials": "DK",
        "bio": "Pioneer in Zero-Trust architecture, BeyondCorp Enterprise, and GCP Workload Identity Federation."
    },
    5: {
        "id": 5,
        "first_name": "Amina",
        "last_name": "Al-Mansoor",
        "role": "Principal Database Engineer",
        "company": "DataScale Systems",
        "linkedin_url": "https://www.linkedin.com/in/amina-almansoor-data",
        "avatar_initials": "AA",
        "bio": "Expert in Cloud Spanner multi-region consistency, BigQuery vector search, and real-time streaming."
    },
    6: {
        "id": 6,
        "first_name": "Kenji",
        "last_name": "Sato",
        "role": "Senior Cloud Data Architect",
        "company": "Google Cloud",
        "linkedin_url": "https://www.linkedin.com/in/kenji-sato-dataflow",
        "avatar_initials": "KS",
        "bio": "Focuses on Apache Beam, Dataflow pipeline optimization, and Pub/Sub enterprise integration patterns."
    },
    7: {
        "id": 7,
        "first_name": "Elena",
        "last_name": "Rostova",
        "role": "VP of Engineering",
        "company": "Serverless Next",
        "linkedin_url": "https://www.linkedin.com/in/elena-rostova-serverless",
        "avatar_initials": "ER",
        "bio": "Building microservices on Cloud Run, Eventarc, and GCP Cloud Functions with 99.99% availability."
    },
    8: {
        "id": 8,
        "first_name": "Marcus",
        "last_name": "Vance",
        "role": "Head of MLOps",
        "company": "AI Scaleup Corp",
        "linkedin_url": "https://www.linkedin.com/in/marcus-vance-mlops",
        "avatar_initials": "MV",
        "bio": "Designs continuous training pipelines, model monitoring dashboards, and Feature Store implementations on GCP."
    },
    9: {
        "id": 9,
        "first_name": "Priya",
        "last_name": "Sharma",
        "role": "Lead FinOps Consultant",
        "company": "Cloud Cost Optimization",
        "linkedin_url": "https://www.linkedin.com/in/priya-sharma-finops",
        "avatar_initials": "PS",
        "bio": "Helps Fortune 500 enterprises optimize GCP commit discounts, CUDs, and BigQuery slot management."
    },
    10: {
        "id": 10,
        "first_name": "Alexandre",
        "last_name": "Dubois",
        "role": "Staff Reliability Engineer",
        "company": "SRE Global",
        "linkedin_url": "https://www.linkedin.com/in/alexandre-dubois-sre",
        "avatar_initials": "AD",
        "bio": "Specializes in Google Cloud Ops Suite, SLO monitoring, Chaos Engineering, and incident response automation."
    }
}

SCHEDULE = [
    {
        "type": "session",
        "id": 101,
        "time": "09:00 AM - 09:45 AM",
        "start_time": "09:00",
        "end_time": "09:45",
        "title": "Next-Gen GenAI: Production Architectures with Gemini 1.5 & Vertex AI",
        "category": "AI & Machine Learning",
        "category_id": "ai_ml",
        "description": "Discover how leading enterprises leverage Vertex AI, Gemini 1.5 Pro multimodal capabilities, and Retrieval-Augmented Generation (RAG) pipelines to build highly secure, low-latency AI applications. Includes live code demonstrations.",
        "room": "Main Keynote Hall (Room A)",
        "speakers": [SPEAKERS[1], SPEAKERS[2]]  # 2 Speakers
    },
    {
        "type": "session",
        "id": 102,
        "time": "09:45 AM - 10:30 AM",
        "start_time": "09:45",
        "end_time": "10:30",
        "title": "Scaling Microservices with GKE Autopilot & Multi-Cluster Mesh",
        "category": "Containers & Serverless",
        "category_id": "containers",
        "description": "Learn hands-on patterns for deploying zero-maintenance Kubernetes clusters with GKE Autopilot, configuring Anthos Service Mesh for cross-region failover, and enforcing pod security standards.",
        "room": "Hall B - Cloud Native",
        "speakers": [SPEAKERS[3]]  # 1 Speaker
    },
    {
        "type": "break",
        "id": 991,
        "time": "10:30 AM - 10:45 AM",
        "title": "Morning Networking & Coffee Break",
        "description": "Enjoy complimentary gourmet coffee, tea, and breakfast pastries in the Expo Lounge while connecting with fellow attendees.",
        "icon": "☕"
    },
    {
        "type": "session",
        "id": 103,
        "time": "10:45 AM - 11:30 AM",
        "start_time": "10:45",
        "end_time": "11:30",
        "title": "Zero-Trust Cloud Security: Workload Identity & BeyondCorp Integration",
        "category": "Security & Governance",
        "category_id": "security",
        "description": "Eliminate service account keys and secure remote access using Workload Identity Federation, GCP Security Command Center Enterprise, and granular IAM conditions across multi-cloud environments.",
        "room": "Room C - Security Suite",
        "speakers": [SPEAKERS[4]]  # 1 Speaker
    },
    {
        "type": "session",
        "id": 104,
        "time": "11:30 AM - 12:15 PM",
        "start_time": "11:30",
        "end_time": "12:15",
        "title": "Global Data at Scale: Multi-Region Spanner & BigQuery Vector Search",
        "category": "Data & Analytics",
        "category_id": "data_analytics",
        "description": "Explore how Cloud Spanner delivers five-nines (99.999%) availability with exact consistency globally, combined with BigQuery's native vector indexing for real-time similarity search on petabytes of data.",
        "room": "Main Keynote Hall (Room A)",
        "speakers": [SPEAKERS[5], SPEAKERS[6]]  # 2 Speakers
    },
    {
        "type": "lunch",
        "id": 992,
        "time": "12:15 PM - 01:15 PM",
        "duration_minutes": 60,
        "title": "🥗 Official Conference Lunch Break (60 Minutes)",
        "description": "Complimentary catered lunch, sponsor booth demonstrations, and table discussions hosted by Google Cloud experts in the Main Dining Atrium.",
        "icon": "🍽️"
    },
    {
        "type": "session",
        "id": 105,
        "time": "01:15 PM - 02:00 PM",
        "start_time": "13:15",
        "end_time": "14:00",
        "title": "Event-Driven Modernization: Cloud Run, Eventarc & Serverless Workflows",
        "category": "Containers & Serverless",
        "category_id": "containers",
        "description": "A deep dive into building event-driven microservices that scale to zero. Learn how to connect Cloud Storage, Pub/Sub, and Firestore events with Eventarc and Cloud Workflows with minimal code overhead.",
        "room": "Hall B - Cloud Native",
        "speakers": [SPEAKERS[7]]  # 1 Speaker
    },
    {
        "type": "session",
        "id": 106,
        "time": "02:00 PM - 02:45 PM",
        "start_time": "14:00",
        "end_time": "14:45",
        "title": "Enterprise MLOps: Automated Vertex Pipelines & Continuous Evaluation",
        "category": "AI & Machine Learning",
        "category_id": "ai_ml",
        "description": "Architect end-to-end Machine Learning pipelines from data ingestion to model deployment using KubeFlow on Vertex AI. Includes model drift monitoring, automated retraining triggers, and CI/CD for AI models.",
        "room": "Main Keynote Hall (Room A)",
        "speakers": [SPEAKERS[8], SPEAKERS[1]]  # 2 Speakers
    },
    {
        "type": "break",
        "id": 993,
        "time": "02:45 PM - 03:00 PM",
        "title": "Afternoon Refreshment Break",
        "description": "Recharge with cold beverages, healthy snacks, and quick speaker Q&A sessions in the Expo Lounge.",
        "icon": "🥤"
    },
    {
        "type": "session",
        "id": 107,
        "time": "03:00 PM - 03:45 PM",
        "start_time": "15:00",
        "end_time": "15:45",
        "title": "Cloud FinOps: Advanced Cost Optimization & Committed Use Discounts",
        "category": "Architecture & Operations",
        "category_id": "architecture",
        "description": "Unpack actionable strategies to cut GCP infrastructure spend by up to 40% using Active Assist recommendations, CUD optimization algorithms, BigQuery edition tuning, and custom billing dashboards.",
        "room": "Room C - FinOps Hub",
        "speakers": [SPEAKERS[9]]  # 1 Speaker
    },
    {
        "type": "session",
        "id": 108,
        "time": "03:45 PM - 04:30 PM",
        "start_time": "15:45",
        "end_time": "16:30",
        "title": "SRE Excellence: SLO Management & Automated Incident Response on GCP",
        "category": "Architecture & Operations",
        "category_id": "architecture",
        "description": "Closing technical session detailing how SRE teams define actionable Service Level Objectives (SLOs), measure error budgets, and automate remediation using Cloud Operations Suite, Audit Logs, and Cloud Functions.",
        "room": "Main Keynote Hall (Room A)",
        "speakers": [SPEAKERS[10], SPEAKERS[2]]  # 2 Speakers
    }
]

def get_all_talks():
    """Return list of all 8 technical talks."""
    return [item for item in SCHEDULE if item.get("type") == "session"]

def get_all_speakers():
    """Return list of all unique speakers sorted by last name."""
    sp_list = list(SPEAKERS.values())
    sp_list.sort(key=lambda s: s["last_name"])
    return sp_list

def get_talk_by_id(talk_id):
    """Return specific talk details by ID."""
    talks = get_all_talks()
    for talk in talks:
        if talk["id"] == talk_id:
            return talk
    return None

def filter_talks(query=None, category=None, speaker_name=None):
    """Filter technical talks based on search query, category, and speaker name."""
    results = get_all_talks()

    if category and category != "all":
        category_lower = category.lower()
        results = [
            t for t in results 
            if t["category_id"].lower() == category_lower or t["category"].lower() == category_lower
        ]

    if speaker_name and speaker_name != "all":
        sp_lower = speaker_name.lower()
        filtered = []
        for t in results:
            for sp in t["speakers"]:
                full_name = f"{sp['first_name']} {sp['last_name']}".lower()
                if sp_lower in full_name or sp_lower in sp["first_name"].lower() or sp_lower in sp["last_name"].lower():
                    filtered.append(t)
                    break
        results = filtered

    if query:
        q = query.strip().lower()
        filtered = []
        for t in results:
            match_text = f"{t['title']} {t['category']} {t['description']} {t['room']}".lower()
            speaker_text = " ".join([f"{s['first_name']} {s['last_name']} {s['company']} {s['role']}" for s in t["speakers"]]).lower()
            
            if q in match_text or q in speaker_text:
                filtered.append(t)
        results = filtered

    return results
