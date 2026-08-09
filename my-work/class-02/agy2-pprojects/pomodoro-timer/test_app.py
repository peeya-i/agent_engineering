import unittest
import os
import sys

# Support vendor packages inside workspace
vendor_dir = os.path.join(os.path.dirname(__file__), 'vendor')
if os.path.exists(vendor_dir):
    sys.path.insert(0, vendor_dir)

from app import app
from storage import load_db, get_all_tasks, add_task, record_session, get_stats, get_settings

class ZenPomodoroTestCase(unittest.TestCase):
    """Unit test suite for Zen Pomodoro Flask App & Storage Logic."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_route(self):
        """Test that index page renders successfully."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Zen Pomodoro", html)
        self.assertIn("Focus Tasks", html)
        self.assertIn("Gentle Rain", html)

    def test_tasks_api_crud(self):
        """Test Task creation, retrieval, updating, and deletion."""
        # 1. Get tasks
        res_list = self.app.get('/api/tasks')
        self.assertEqual(res_list.status_code, 200)
        initial_tasks = res_list.get_json()
        self.assertIsInstance(initial_tasks, list)

        # 2. Create task
        res_create = self.app.post('/api/tasks', json={
            "title": "Unit Test Task",
            "category": "Study",
            "est_pomodoros": 3
        })
        self.assertEqual(res_create.status_code, 201)
        created_task = res_create.get_json()
        self.assertEqual(created_task["title"], "Unit Test Task")
        self.assertEqual(created_task["category"], "Study")
        self.assertEqual(created_task["est_pomodoros"], 3)
        task_id = created_task["id"]

        # 3. Update task
        res_update = self.app.put(f'/api/tasks/{task_id}', json={
            "completed": True,
            "is_active": True
        })
        self.assertEqual(res_update.status_code, 200)
        updated_task = res_update.get_json()
        self.assertTrue(updated_task["completed"])
        self.assertTrue(updated_task["is_active"])

        # 4. Delete task
        res_delete = self.app.delete(f'/api/tasks/{task_id}')
        self.assertEqual(res_delete.status_code, 200)
        self.assertTrue(res_delete.get_json()["success"])

    def test_session_and_stats_api(self):
        """Test recording focus sessions and updating stats."""
        res_session = self.app.post('/api/sessions', json={
            "task_id": "t1",
            "duration_minutes": 25,
            "type": "focus"
        })
        self.assertEqual(res_session.status_code, 200)
        data = res_session.get_json()
        self.assertIn("session", data)
        self.assertIn("stats", data)
        self.assertGreater(data["stats"]["total_focus_minutes"], 0)

        # Check GET /api/stats
        res_stats = self.app.get('/api/stats')
        self.assertEqual(res_stats.status_code, 200)
        stats = res_stats.get_json()
        self.assertIn("total_focus_minutes", stats)
        self.assertIn("total_sessions", stats)

    def test_settings_api(self):
        """Test settings retrieval and update."""
        res_get = self.app.get('/api/settings')
        self.assertEqual(res_get.status_code, 200)
        
        res_update = self.app.post('/api/settings', json={
            "focus_duration": 30,
            "short_break_duration": 10,
            "theme": "nordic-fog"
        })
        self.assertEqual(res_update.status_code, 200)
        settings = res_update.get_json()
        self.assertEqual(settings["focus_duration"], 30)
        self.assertEqual(settings["short_break_duration"], 10)
        self.assertEqual(settings["theme"], "nordic-fog")

    def test_health_endpoint(self):
        """Test health check endpoint."""
        res = self.app.get('/health')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "healthy")

if __name__ == '__main__':
    unittest.main()
