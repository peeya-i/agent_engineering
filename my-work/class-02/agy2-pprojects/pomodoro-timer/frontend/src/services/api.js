/**
 * Centralized REST API Client for Zen Pomodoro Backend
 */

export async function fetchTasks() {
  const res = await fetch('/api/tasks');
  if (!res.ok) throw new Error('Failed to fetch tasks');
  return res.json();
}

export async function createTask(title, category = 'Work', est_pomodoros = 1) {
  const res = await fetch('/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, category, est_pomodoros })
  });
  if (!res.ok) throw new Error('Failed to create task');
  return res.json();
}

export async function updateTask(taskId, updates) {
  const res = await fetch(`/api/tasks/${taskId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });
  if (!res.ok) throw new Error('Failed to update task');
  return res.json();
}

export async function deleteTask(taskId) {
  const res = await fetch(`/api/tasks/${taskId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete task');
  return res.json();
}

export async function recordSession(taskId, durationMinutes, sessionType) {
  const res = await fetch('/api/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      task_id: taskId,
      duration_minutes: durationMinutes,
      type: sessionType
    })
  });
  if (!res.ok) throw new Error('Failed to record session');
  return res.json();
}

export async function fetchStats() {
  const res = await fetch('/api/stats');
  if (!res.ok) throw new Error('Failed to fetch stats');
  return res.json();
}

export async function fetchSettings() {
  const res = await fetch('/api/settings');
  if (!res.ok) throw new Error('Failed to fetch settings');
  return res.json();
}

export async function updateSettings(settings) {
  const res = await fetch('/api/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings)
  });
  if (!res.ok) throw new Error('Failed to update settings');
  return res.json();
}
