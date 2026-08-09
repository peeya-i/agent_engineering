import os
import sys
import unittest

vendor_dir = os.path.join(os.path.dirname(__file__), 'vendor')
if os.path.exists(vendor_dir):
    sys.path.insert(0, vendor_dir)

from app import app
from data import SCHEDULE, get_all_talks, get_all_speakers, filter_talks


class CloudConAppTestCase(unittest.TestCase):
    """Test suite for CloudCon 2026 Flask Application & Data Integrity."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_route(self):
        """Test that homepage loads successfully with HTTP 200."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        html_content = response.data.decode('utf-8')
        self.assertIn("CloudCon 2026", html_content)
        self.assertIn("Google Cloud Innovations", html_content)
        self.assertIn("Official Conference Lunch Break (60 Minutes)", html_content)

    def test_total_talks_count(self):
        """Requirement: The 1-day event must have a list of exactly 8 talks in total."""
        talks = get_all_talks()
        self.assertEqual(len(talks), 8, f"Expected 8 talks, got {len(talks)}")

    def test_max_speakers_per_talk(self):
        """Requirement: Each talk has 1 or 2 max speakers."""
        talks = get_all_talks()
        for talk in talks:
            speakers = talk.get("speakers", [])
            self.assertTrue(1 <= len(speakers) <= 2, 
                            f"Talk '{talk['title']}' has {len(speakers)} speakers, expected 1 or 2.")

    def test_speaker_fields(self):
        """Requirement: Each speaker has First Name, Last Name and LinkedIn url."""
        speakers = get_all_speakers()
        self.assertGreater(len(speakers), 0)
        for sp in speakers:
            self.assertIn("first_name", sp)
            self.assertIn("last_name", sp)
            self.assertIn("linkedin_url", sp)
            self.assertTrue(sp["first_name"], "First name cannot be empty")
            self.assertTrue(sp["last_name"], "Last name cannot be empty")
            self.assertTrue(sp["linkedin_url"].startswith("https://www.linkedin.com/"), 
                            f"Invalid LinkedIn URL: {sp['linkedin_url']}")

    def test_talk_attributes(self):
        """Requirement: Talk has ID, Title, Speakers, Category, Description and time."""
        talks = get_all_talks()
        for talk in talks:
            self.assertIn("id", talk)
            self.assertIn("title", talk)
            self.assertIn("speakers", talk)
            self.assertIn("category", talk)
            self.assertIn("description", talk)
            self.assertIn("time", talk)

    def test_lunch_break_duration(self):
        """Requirement: 60-minute lunch break in schedule."""
        lunch_items = [item for item in SCHEDULE if item.get("type") == "lunch"]
        self.assertEqual(len(lunch_items), 1, "Should have 1 official lunch break")
        lunch = lunch_items[0]
        self.assertEqual(lunch.get("duration_minutes"), 60, "Lunch break must be 60 minutes")
        self.assertIn("12:15 PM - 01:15 PM", lunch["time"])

    def test_api_talks_search_filtering(self):
        """Requirement: Allow users to search by category, speaker, title."""
        # Category filter test
        res_cat = self.app.get('/api/talks?category=ai_ml')
        self.assertEqual(res_cat.status_code, 200)
        data_cat = res_cat.get_json()
        self.assertGreater(data_cat["count"], 0)
        for t in data_cat["talks"]:
            self.assertEqual(t["category_id"], "ai_ml")

        # Speaker filter test
        res_sp = self.app.get('/api/talks?speaker=Mendoza')
        self.assertEqual(res_sp.status_code, 200)
        data_sp = res_sp.get_json()
        self.assertGreater(data_sp["count"], 0)
        
        # Keyword search test
        res_q = self.app.get('/api/talks?q=Kubernetes')
        self.assertEqual(res_q.status_code, 200)
        data_q = res_q.get_json()
        self.assertGreater(data_q["count"], 0)

    def test_api_talk_detail(self):
        """Test detail API endpoint for talk ID 101."""
        response = self.app.get('/api/talk/101')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], 101)
        self.assertIn("Next-Gen GenAI", data["title"])

        # Test non-existent talk ID
        res_404 = self.app.get('/api/talk/9999')
        self.assertEqual(res_404.status_code, 404)

if __name__ == '__main__':
    unittest.main()
