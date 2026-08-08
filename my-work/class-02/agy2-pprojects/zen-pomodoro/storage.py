import os
import json
import uuid
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DB_FILE = os.path.join(DATA_DIR, 'db.json')

DEFAULT_DATA = {
    "settings": {
        "focus_duration": 25,
        "short_break_duration": 5,
        "long_break_duration": 15,
        "long_break_interval": 4,
        "auto_start_breaks": False,
        "auto_start_pomodoros": False,
        "sound_enabled": True,
        "sound_volume": 0.5,
        "theme": "serene-forest"
    },
    "tasks": [
        {
            "id": "t1",
            "title": "Design calm UI components",
            "category": "Design",
            "est_pomodoros": 4,
            "completed_pomodoros": 2,
            "completed": False,
            "is_active": True,
            "created_at": "2026-07-25T09:00:00"
        },
        {
            "id": "t2",
            "title": "Review system architecture documentation",
            "category": "Work",
            "est_pomodoros": 2,
            "completed_pomodoros": 1,
            "completed": False,
            "is_active": False,
            "created_at": "2026-07-25T09:30:00"
        },
        {
            "id": "t3",
            "title": "Daily mindfulness meditation & journaling",
            "category": "Personal",
            "est_pomodoros": 1,
            "completed_pomodoros": 1,
            "completed": True,
            "is_active": False,
            "created_at": "2026-07-25T08:00:00"
        }
    ],
    "sessions": [
        {
            "id": "s1",
            "task_id": "t1",
            "duration_minutes": 25,
            "type": "focus",
            "timestamp": "2026-07-25T09:25:00"
        },
        {
            "id": "s2",
            "task_id": "t1",
            "duration_minutes": 25,
            "type": "focus",
            "timestamp": "2026-07-25T10:00:00"
        },
        {
            "id": "s3",
            "task_id": "t2",
            "duration_minutes": 25,
            "type": "focus",
            "timestamp": "2026-07-25T10:35:00"
        }
    ]
}

def save_db(data):
    """Save data to db.json file directly."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def ensure_db():
    """Ensure data directory and db.json exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DB_FILE):
        save_db(DEFAULT_DATA)

def load_db():
    """Load JSON data database."""
    ensure_db()
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA

# --- Tasks CRUD ---

def get_all_tasks():
    db = load_db()
    return db.get("tasks", [])

def add_task(title, category="Work", est_pomodoros=1):
    db = load_db()
    new_task = {
        "id": f"t_{uuid.uuid4().hex[:8]}",
        "title": title.strip(),
        "category": category,
        "est_pomodoros": int(est_pomodoros),
        "completed_pomodoros": 0,
        "completed": False,
        "is_active": len(db["tasks"]) == 0,
        "created_at": datetime.now().isoformat()
    }
    db["tasks"].append(new_task)
    save_db(db)
    return new_task

def update_task(task_id, updates):
    db = load_db()
    for task in db["tasks"]:
        if task["id"] == task_id:
            for key in ["title", "category", "est_pomodoros", "completed_pomodoros", "completed", "is_active"]:
                if key in updates:
                    task[key] = updates[key]
            
            if updates.get("is_active"):
                for t in db["tasks"]:
                    if t["id"] != task_id:
                        t["is_active"] = False
            break
    save_db(db)
    return get_task_by_id(task_id)

def get_task_by_id(task_id):
    db = load_db()
    for task in db["tasks"]:
        if task["id"] == task_id:
            return task
    return None

def delete_task(task_id):
    db = load_db()
    db["tasks"] = [t for t in db["tasks"] if t["id"] != task_id]
    save_db(db)
    return True

# --- Sessions & Stats ---

def record_session(task_id=None, duration_minutes=25, session_type="focus"):
    db = load_db()
    new_session = {
        "id": f"s_{uuid.uuid4().hex[:8]}",
        "task_id": task_id,
        "duration_minutes": duration_minutes,
        "type": session_type,
        "timestamp": datetime.now().isoformat()
    }
    db["sessions"].append(new_session)

    if session_type == "focus" and task_id:
        for task in db["tasks"]:
            if task["id"] == task_id:
                task["completed_pomodoros"] += 1
                break

    save_db(db)
    return new_session

def get_stats():
    db = load_db()
    sessions = db.get("sessions", [])
    focus_sessions = [s for s in sessions if s.get("type") == "focus"]
    
    total_minutes = sum(s.get("duration_minutes", 0) for s in focus_sessions)
    total_sessions = len(focus_sessions)
    completed_tasks = len([t for t in db.get("tasks", []) if t.get("completed")])
    
    return {
        "total_focus_minutes": total_minutes,
        "total_sessions": total_sessions,
        "completed_tasks": completed_tasks,
        "recent_sessions": sessions[-10:]
    }

# --- Settings ---

def get_settings():
    db = load_db()
    return db.get("settings", DEFAULT_DATA["settings"])

def update_settings(new_settings):
    db = load_db()
    db["settings"].update(new_settings)
    save_db(db)
    return db["settings"]
