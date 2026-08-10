import os
import sys

# Support vendor packages inside workspace
vendor_dir = os.path.join(os.path.dirname(__file__), 'vendor')
if os.path.exists(vendor_dir):
    sys.path.insert(0, vendor_dir)

from flask import Flask, render_template, jsonify, request
from storage import (
    get_all_tasks, add_task, update_task, delete_task,
    record_session, get_stats, get_settings, update_settings
)

dist_dir = os.path.join(os.path.dirname(__file__), 'dist')
static_folder = dist_dir if os.path.exists(dist_dir) else 'static'
template_folder = dist_dir if os.path.exists(dist_dir) else 'templates'

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder, static_url_path='')

@app.route('/')
def index():
    """Render Zen Pomodoro main single-page application."""
    if os.path.exists(os.path.join(dist_dir, 'index.html')):
        return app.send_static_file('index.html')
    tasks = get_all_tasks()
    stats = get_stats()
    settings = get_settings()
    return render_template('index.html', tasks=tasks, stats=stats, settings=settings)


# --- Tasks API ---

@app.route('/api/tasks', methods=['GET'])
def api_tasks_list():
    """Get all tasks."""
    return jsonify(get_all_tasks())

@app.route('/api/tasks', methods=['POST'])
def api_tasks_create():
    """Create a new task."""
    data = request.json or {}
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    category = data.get('category', 'Work')
    est_pomodoros = int(data.get('est_pomodoros', 1))
    new_task = add_task(title, category=category, est_pomodoros=est_pomodoros)
    return jsonify(new_task), 201

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def api_tasks_update(task_id):
    """Update task details (completed status, active status, etc)."""
    data = request.json or {}
    updated = update_task(task_id, data)
    if not updated:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(updated)

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def api_tasks_delete(task_id):
    """Delete a task."""
    success = delete_task(task_id)
    return jsonify({'success': success})

# --- Sessions & Stats API ---

@app.route('/api/sessions', methods=['POST'])
def api_sessions_record():
    """Record a completed focus or break session."""
    data = request.json or {}
    task_id = data.get('task_id')
    duration = int(data.get('duration_minutes', 25))
    session_type = data.get('type', 'focus')
    
    session = record_session(task_id=task_id, duration_minutes=duration, session_type=session_type)
    return jsonify({
        'session': session,
        'stats': get_stats(),
        'tasks': get_all_tasks()
    })

@app.route('/api/stats', methods=['GET'])
def api_stats_get():
    """Retrieve aggregate productivity stats."""
    return jsonify(get_stats())

# --- Settings API ---

@app.route('/api/settings', methods=['GET'])
def api_settings_get():
    """Retrieve app settings."""
    return jsonify(get_settings())

@app.route('/api/settings', methods=['POST'])
def api_settings_update():
    """Update user timer durations and aesthetic preferences."""
    data = request.json or {}
    updated = update_settings(data)
    return jsonify(updated)

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'app': 'Zen Pomodoro Productivity App',
        'tasks_count': len(get_all_tasks())
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)

