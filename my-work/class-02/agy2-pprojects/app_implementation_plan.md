# Implementation Plan - Zen Pomodoro: Calm & Aesthetic Productivity Application

Build a serene, aesthetic, and feature-rich Pomodoro productivity web application called **Zen Pomodoro**. The app combines a customizable focus timer, task management with session tracking, ambient Web Audio soundscapes, productivity statistics, and customizable soothing color themes.

---

## User Review Required

> [!IMPORTANT]
> - **Tech Stack**: Python 3 + Flask backend serving a responsive single-page web application.
> - **Design Aesthetics**: Calm, soothing glassmorphism with soft pastel gradients, glowing circular progress ring, and ambient sound generator (Web Audio API).
> - **Port**: Flask server will run on `http://127.0.0.1:5000`.

---

## Proposed Changes

Project Location: `/home/pi-net/Documents/Antigravity/agy2-projects/zen-pomodoro`

### Backend (`Python / Flask`)

#### [NEW] `zen-pomodoro/app.py`
- Flask server providing web routes and REST APIs for persistent tasks, focus sessions, and settings.
- REST API Endpoints:
  - `GET /`: Serves the primary single-page application.
  - `GET /api/tasks`, `POST /api/tasks`, `PUT /api/tasks/<id>`, `DELETE /api/tasks/<id>`: Manage task items (Title, Category, Target Pomodoros, Completed Pomodoros, Status).
  - `GET /api/stats`, `POST /api/stats/session`: Record and retrieve focus statistics (Total minutes, Completed sessions, Daily breakdown).
  - `GET /api/settings`, `POST /api/settings`: Save timer durations and theme preferences.
  - `GET /health`: Health check.

#### [NEW] `zen-pomodoro/storage.py`
- Lightweight JSON file-based data storage module (`data/db.json`) ensuring user tasks, session history, and preferences persist across restarts.

#### [NEW] `zen-pomodoro/test_app.py`
- Unit test suite verifying task CRUD operations, session recording, statistics calculations, and API endpoints.

---

### Frontend (`HTML5 / Vanilla CSS / Vanilla JS`)

#### [NEW] `zen-pomodoro/templates/index.html`
- Serene HTML5 layout featuring:
  - **Timer View**: Circular SVG SVG progress ring with large minimalist timer countdown, session mode toggle (*Focus*, *Short Break*, *Long Break*), Play/Pause/Skip controls, active task badge.
  - **Active Task Header**: Highlighted current task being worked on with cycle counter (`2 / 4 🍅`).
  - **Task Manager Panel**: Add new task with category tags (*Work*, *Study*, *Design*, *Personal*), estimated Pomodoros, completion checkboxes, and quick active task selector.
  - **Ambient Soundscape Bar**: Toggle procedural ambient sounds (*Rain*, *Gentle Wind*, *Soft Pink Noise*, *Ocean Waves*, *Zen Bowl Chime*) built with Web Audio API (no external file dependencies).
  - **Productivity Analytics & Streak**: Daily focus minutes counter, completed session count, weekly focus breakdown visual cards.
  - **Theme & Timer Settings Modal**: Custom focus/break lengths, auto-start options, and theme switcher (*Serene Forest*, *Nordic Fog*, *Sunset Calm*, *Cherry Blossom*, *Midnight Obsidian*).

#### [NEW] `zen-pomodoro/static/css/style.css`
- Modern calm design system with HSL pastel color tokens, glassmorphism card containers, smooth transitions, ambient gradient backgrounds, and responsive layout.

#### [NEW] `zen-pomodoro/static/js/audio.js`
- Web Audio API synthesizer module providing ambient noise generators (Rain, Wind, Ocean, Binaural tone) and soothing chime bell notifications upon session completion.

#### [NEW] `zen-pomodoro/static/js/timer.js` & `static/js/app.js`
- Pomodoro timer state machine, browser notifications, task syncing, session log saving, and theme switching.

---

### Documentation

#### [NEW] `zen-pomodoro/README.md`
- Complete guide on installation, running the server, test suite execution, feature overview, and code organization.

---

## Verification Plan

### Automated Tests
- Run `PYTHONPATH=./vendor python3 -m unittest test_app.py -v` to test storage persistence, task CRUD endpoints, and stats recording.

### Manual & Server Verification
1. Launch Flask server via `python3 app.py` on port 5000.
2. Verify HTTP status, test task creation, timer execution, theme switching, and ambient audio generation.
