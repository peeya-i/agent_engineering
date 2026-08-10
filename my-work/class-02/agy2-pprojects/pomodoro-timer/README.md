# 🧘 Zen Pomodoro — Serene Productivity Application

A calm, aesthetic, and feature-rich Pomodoro productivity web application built with a modern **Vite + React** frontend framework architecture, **Vanilla CSS (Glassmorphism & Pastel Themes)**, **Web Audio API Soundscapes**, and a **Python (Flask)** REST API backend.

---

## 🌟 Key Features

- 🧘 **Customizable Pomodoro Timer**: Switch effortlessly between *Focus* (25 min default), *Short Break* (5 min default), and *Long Break* (15 min default). Includes an SVG circular progress ring and document title countdown.
- 🎨 **5 Calm Aesthetic Color Themes**: Toggle between *Serene Forest*, *Nordic Fog*, *Sunset Calm*, *Cherry Blossom*, and *Midnight Obsidian*.
- 🔊 **Procedural Web Audio Ambient Soundscapes**: Built-in sound generator producing *Gentle Rain*, *Soft Wind*, *Ocean Waves*, and *Alpha Focus Beats* directly via the Web Audio API.
- 🔔 **Zen Bowl Completion Chime**: Soft 432 Hz dual sine harmonic chime notification when a focus session completes.
- 📋 **Task Management & Session Tracking**: Add, categorize (*Work*, *Study*, *Design*, *Personal*), prioritize, and track completed vs target Pomodoro cycles per task (`2 / 4 🍅`).
- 📊 **Productivity Statistics**: Real-time summary of total focus minutes, completed sessions, and finished tasks stored persistently in a local JSON database.
- ⚛️ **Modern Component Architecture**: Built with Vite, React Context state management (`TaskContext`, `TimerContext`), and modular component rendering.

---

## 🛠️ Project Structure

```text
zen-pomodoro/
├── app.py              # Flask server & REST API endpoints
├── storage.py          # Data persistence module (data/db.json)
├── test_app.py         # Unit test suite
├── package.json        # Frontend dependencies & scripts
├── vite.config.js      # Vite build & proxy config
├── frontend/           # Modern React SPA Source Directory
│   ├── index.html      # Vite HTML entrypoint
│   └── src/
│       ├── main.jsx    # React mounting entrypoint
│       ├── App.jsx     # Main layout container
│       ├── audio/      # Web Audio API ES module engine
│       ├── context/    # TimerContext & TaskContext state providers
│       ├── services/   # REST API client
│       ├── styles/     # Glassmorphism design system & pastel theme tokens
│       └── components/ # Reusable UI components (TimerRing, TaskManager, StatsGrid, etc.)
├── dist/               # Production build output
└── data/
    └── db.json         # Local persistent data database
```

---

## 🚀 Quick Setup & Execution Guide

### Step 1: Install Dependencies
```bash
npm install
```

### Step 2: Run Development Mode (Vite Dev Server + Flask REST API)
Start the Flask backend:
```bash
python3 app.py
```

In a separate terminal, start Vite frontend HMR:
```bash
npm run dev
```
👉 Open **`http://localhost:3000`** for live hot-reloading development.

### Step 3: Build for Production
```bash
npm run build
```
Flask will serve the compiled bundle from `dist/` directly at **`http://127.0.0.1:5001`**.



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
