import os
import tempfile
import unittest
from app import create_app

class GymAppTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.app = create_app()
        self.app.config.update(TESTING=True, DATABASE=self.tmp.name)
        # Initialize schema for the test database.
        with self.app.app_context():
            from app.db import init_db
            init_db()
        self.client = self.app.test_client()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_dashboard_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

    def test_members_page_loads(self):
        response = self.client.get("/members")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add a member", response.data)

    def test_member_can_be_created(self):
        response = self.client.post("/members", data={
            "full_name": "Test Member",
            "email": "test.member@example.com",
            "phone": "1234567890",
            "gender": "Prefer not to say",
            "status": "Active"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Member", response.data)

if __name__ == "__main__":
    unittest.main()
