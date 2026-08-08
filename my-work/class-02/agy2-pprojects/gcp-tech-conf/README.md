# ☁️ CloudCon 2026: Google Cloud Innovations Conference Website

A modern, high-performance 1-day technical conference informational web application built with **Python**, **Flask**, **HTML5**, **Vanilla CSS (Glassmorphism Dark Design System)**, and **JavaScript**.

---

## 🌟 Features & Requirements Summary

- 📅 **1-Day Schedule & Timetable**: Displays event date (`October 15, 2026`), location, and full schedule with timeline and grid view options.
- 🎤 **8 Technical Talks**: Covers Google Cloud topics including Gemini 1.5, Vertex AI, GKE Autopilot, Cloud Spanner, Pub/Sub, Eventarc, FinOps, and SRE.
- 👥 **Max 1–2 Speakers Per Talk**: Each talk has 1 or 2 featured expert speakers with First Name, Last Name, Role, Company, and LinkedIn profile URLs.
- 🏷️ **Categorization**: Talks tagged under 5 categories (*AI & Machine Learning*, *Containers & Serverless*, *Data & Analytics*, *Security & Governance*, *Architecture & Operations*).
- 🔍 **Interactive Search & Filter**: Instant client-side & server-side filtering by category, speaker, or keyword query.
- 🍽️ **60-Minute Lunch Break**: Highlighted catered lunch break from 12:15 PM – 1:15 PM PST in the schedule.
- 💡 **Interactive Talk Modals**: Click any talk to open a detailed modal overlay with speaker bios and LinkedIn links.
- 🧪 **Comprehensive Test Suite**: Automated unit tests for all endpoints and data integrity rules.

---

## 🛠️ Project Architecture

```text
gcp-tech-conf/
├── app.py              # Flask server entrypoint & REST API endpoints
├── data.py             # Event metadata, 8 technical talks, speakers, & filter logic
├── test_app.py         # Automated PyTest / Unittest test suite
├── README.md           # Setup, run, and development documentation
├── templates/
│   └── index.html      # Main conference single-page template
└── static/
    ├── css/
    │   └── style.css   # Google Cloud design system (dark glassmorphism, animations)
    └── js/
        └── main.js     # Search, filter, view switcher, & modal interactions
```

---

## 🚀 Quick Setup & Installation Guide

### Prerequisites
- **Python 3.8+** installed on Linux, macOS, or Windows.
- **pip** package installer.

### Step 1: Clone / Navigate to Directory
```bash
cd /home/pi-net/Documents/Antigravity/agy2-projects/gcp-tech-conf
```

### Step 2: (Optional) Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install flask
```

---

## 🖥️ Running the Application

Start the Flask development web server:

```bash
python3 app.py
```

The application will start running at:
👉 **`http://127.0.0.1:5000`** (or `http://localhost:5000`)

---

## 🧪 Running Automated Tests

Run the unit test suite to verify route responses, 8-talk requirement, max-2 speaker rules, 60-min lunch break, and search filters:

```bash
python3 -m unittest test_app.py -v
```

---

## 🔌 REST API Reference

| Endpoint | Method | Parameters | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | — | Renders main conference homepage UI |
| `/api/talks` | `GET` | `q` (string), `category` (string), `speaker` (string) | Returns filtered list of technical talks in JSON format |
| `/api/talk/<id>` | `GET` | `id` (int) | Returns JSON details for a specific talk |
| `/health` | `GET` | — | Health check endpoint returning service status |

### Example API Request:
```bash
curl "http://127.0.0.1:5000/api/talks?category=ai_ml&q=Gemini"
```

---

## 🔧 How to Make Further Changes

### 1. Adding or Modifying Talks / Speakers
All dummy data is maintained in `data.py`:
- **Add a Speaker**: Add a new entry to the `SPEAKERS` dictionary with `first_name`, `last_name`, `role`, `company`, `linkedin_url`, `avatar_initials`, and `bio`.
- **Add or Edit a Talk**: Modify `SCHEDULE` in `data.py`. Ensure the `type` is `"session"` and `speakers` list contains 1 or 2 speaker objects.

### 2. Changing the Lunch Break or Schedule Times
In `data.py`, update the entry where `"type": "lunch"` to adjust the time or duration:
```python
{
    "type": "lunch",
    "id": 992,
    "time": "12:15 PM - 01:15 PM",
    "duration_minutes": 60,
    "title": "🥗 Official Conference Lunch Break (60 Minutes)",
    "description": "Complimentary catered lunch..."
}
```

### 3. Modifying Styling & Aesthetics
Styles are located in `static/css/style.css`.
- Core CSS variables (colors, radii, shadows) are defined under `:root`.
- Modify Google Cloud accent colors (`--gcp-blue`, `--gcp-cyan`, `--gcp-green`, `--gcp-purple`) to tweak the visual aesthetic.

---

## 📄 License
Created for Google Cloud Tech Conference 2026 demonstration.
