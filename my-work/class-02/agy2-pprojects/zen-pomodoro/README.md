# 🧘 Zen Pomodoro — Serene Productivity Application

A calm, aesthetic, and feature-rich Pomodoro productivity web application built with **Python (Flask)**, **HTML5**, **Vanilla CSS (Glassmorphism & Pastel Themes)**, and **JavaScript (Web Audio API Soundscapes)**.

---

## 🌟 Key Features

- 🧘 **Customizable Pomodoro Timer**: Switch effortlessly between *Focus* (25 min default), *Short Break* (5 min default), and *Long Break* (15 min default). Includes an SVG circular progress ring and document title countdown.
- 🎨 **5 Calm Aesthetic Color Themes**: Toggle between *Serene Forest*, *Nordic Fog*, *Sunset Calm*, *Cherry Blossom*, and *Midnight Obsidian*.
- 🔊 **Procedural Web Audio Ambient Soundscapes**: Built-in sound generator producing *Gentle Rain*, *Soft Wind*, *Ocean Waves*, and *Alpha Focus Beats* directly via the Web Audio API (no external file dependencies).
- 🔔 **Zen Bowl Completion Chime**: Soft 432 Hz dual sine harmonic chime notification when a focus session completes.
- 📋 **Task Management & Session Tracking**: Add, categorize (*Work*, *Study*, *Design*, *Personal*), prioritize, and track completed vs target Pomodoro cycles per task (`2 / 4 🍅`).
- 📊 **Productivity Statistics**: Real-time summary of total focus minutes, completed sessions, and finished tasks stored persistently in a local JSON database.
- 🧪 **Unit Test Suite**: Full test coverage of routes, storage persistence, CRUD APIs, and settings.

---

## 🛠️ Project Structure

```text
zen-pomodoro/
├── app.py              # Flask server & REST API endpoints
├── storage.py          # Data persistence module (data/db.json)
├── test_app.py         # Unit test suite
├── README.md           # Setup & development documentation
├── data/
│   └── db.json         # Local persistent data database
├── templates/
│   └── index.html      # Single-page application HTML5 layout
└── static/
    ├── css/
    │   └── style.css   # Glassmorphism design system & pastel theme variables
    └── js/
        ├── audio.js    # Web Audio API soundscape synth engine & Zen bowl chime
        └── app.js      # Timer state machine, task manager, stats, & theme controller
```

---

## 🚀 Quick Setup & Execution Guide

### Prerequisites
- **Python 3.8+**
- **pip** package installer

### Step 1: Navigate to Project Directory
```bash
cd /home/pi-net/Documents/Antigravity/agy2-projects/zen-pomodoro
```

### Step 2: (Optional) Install Flask
If Flask is not already installed in your Python environment:
```bash
python3 -m pip install flask --target ./vendor
```

### Step 3: Run the Application
```bash
python3 app.py
```

The application will start running at:
👉 **`http://127.0.0.1:5001`** (or `http://localhost:5001`)


---

## 🧪 Running Unit Tests

Run the test suite to verify task CRUD, stats calculations, timer settings, and health check endpoints:

```bash
python3 -m unittest test_app.py -v
```

---

## 🔌 REST API Reference

| Endpoint | Method | Payload / Params | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | — | Renders main Zen Pomodoro web application |
| `/api/tasks` | `GET` | — | Returns list of all task items |
| `/api/tasks` | `POST` | `{ title, category, est_pomodoros }` | Creates a new task item |
| `/api/tasks/<id>` | `PUT` | `{ completed, is_active, title, ... }` | Updates task state or marks active |
| `/api/tasks/<id>` | `DELETE` | — | Deletes a task item |
| `/api/sessions` | `POST` | `{ task_id, duration_minutes, type }` | Records completed session and updates stats |
| `/api/stats` | `GET` | — | Returns aggregate productivity statistics |
| `/api/settings` | `GET` / `POST` | `{ focus_duration, theme, ... }` | Gets or updates timer durations and themes |
| `/health` | `GET` | — | Returns server health status |

---

## 🎨 Theme Customization

Themes are defined as CSS variable tokens in `static/css/style.css`.
To add a custom palette, add a new `[data-theme="my-theme"]` block in `style.css` specifying:
- `--bg-gradient`: Background radial/linear gradient
- `--card-bg`: Glassmorphism container background
- `--accent-primary`: Primary glowing accent color
- `--text-main`: Primary text color
- `--text-muted`: Subtitle and label text color

---

## 📄 License
Created for Zen Pomodoro Productivity Application.
