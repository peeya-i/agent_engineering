# Implementation Plan - Google Cloud Tech Conference (CloudCon 2026) 1-Day Informational Website

Build a premium, modern 1-day technical conference website for "CloudCon 2026: Google Cloud Innovations", using Python & Flask on the backend with plain HTML, CSS, and JavaScript on the frontend.

## User Review Required

> [!IMPORTANT]
> - **Tech Stack**: Python 3 + Flask framework.
> - **Schedule Structure**: 8 technical talks + 60-minute lunch break + morning/afternoon coffee breaks.
> - **Port**: Flask server will run on `http://127.0.0.1:5000` (or `0.0.0.0:5000`).

## Proposed Changes

Project Location: `/home/pi-net/Documents/Antigravity/agy2-projects/gcp-tech-conf`

### Backend (`Python / Flask`)

#### [NEW] `gcp-tech-conf/app.py`
- Main Flask application entrypoint.
- Routes:
  - `/`: Main homepage rendering event info, date, venue location, schedule, speakers, and search UI.
  - `/api/talks`: REST API endpoint accepting query parameters (`q`, `category`, `speaker`) returning filtered JSON data.
  - `/api/talk/<int:talk_id>`: REST API returning detailed talk & speaker modal data.
  - `/health`: Health check endpoint.

#### [NEW] `gcp-tech-conf/data.py`
- Holds dummy conference data structures:
  - Event Metadata: Title, Date, Venue, Location, City, Timezone, Description.
  - Categories: `AI & Machine Learning`, `Containers & Cloud Native`, `Databases & Analytics`, `Security & Identity`, `Architecture & Operations`.
  - Speakers: First Name, Last Name, Role, Company, LinkedIn URL, Avatar/Initials.
  - 8 Technical Talks (each with ID, Title, Category, Description, Start Time, End Time, Room, and 1 or 2 speakers max).
  - Built-in 60-minute Lunch Break (12:15 PM - 1:15 PM).

#### [NEW] `gcp-tech-conf/test_app.py`
- Pytest/unittest test suite covering:
  - Homepage route loading & HTTP 200 response.
  - API endpoints `/api/talks` filtering by title, category, and speaker.
  - Talk detail endpoint `/api/talk/<id>`.
  - Data validation (ensuring 8 talks, max 2 speakers per talk, lunch break present).

---

### Frontend (`HTML5 / Vanilla CSS / Vanilla JS`)

#### [NEW] `gcp-tech-conf/templates/index.html`
- Modern, accessible HTML5 layout featuring:
  - Hero Header with Event Title, Date (`October 15, 2026`), Location (`San Francisco, CA & Virtual`), and Quick Stats.
  - Search & Filter bar: Keyword search input, Category pills/dropdown, Speaker filter, View toggle (Schedule Timeline vs Grid cards).
  - Timetable / Schedule view with highlighted 60-minute Lunch Break badge.
  - Talk Cards / Items with category tags, time badges, speaker tags, LinkedIn buttons, and interactive modal trigger.
  - Speaker Directory section displaying speaker bios & LinkedIn profiles.
  - Venue & Location map/details section.
  - Modal window for deep dive talk descriptions.

#### [NEW] `gcp-tech-conf/static/css/style.css`
- Modern design system based on Google Cloud color palette (Deep Navy, Cloud Blue, Vibrant Teal, Accent Yellow/Green).
- Dark/Light theme support, glassmorphism cards, micro-animations, hover effects, and responsive breakpoints for mobile/desktop.

#### [NEW] `gcp-tech-conf/static/js/main.js`
- Real-time client-side search & filtering with debounced input.
- Seamless AJAX fetching fallback to local state for fast UI feedback.
- Interactive modal dialogs for full talk details.
- View switcher (Timeline view vs Grid view).

---

### Documentation & Setup

#### [NEW] `gcp-tech-conf/README.md`
- Comprehensive guide on environment setup (`venv`), dependency installation (`pip install flask`), running the application, running test suite, data schema details, and extending the app.

---

## Verification Plan

### Automated Tests
- Run `python3 -m unittest test_app.py` to test routes, filters, search logic, and data structure integrity.

### Manual Verification & Launch
1. Start Flask web server using `python3 app.py`.
2. Verify HTTP responses using `curl http://127.0.0.1:5000/` and `curl http://127.0.0.1:5000/api/talks?category=AI%20%26%20Machine%20Learning`.
3. Check all search filters (Category, Speaker, Title keyword) and ensure the 60-min lunch break displays clearly.
