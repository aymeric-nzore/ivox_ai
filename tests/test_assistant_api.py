import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app


class AssistantApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_returns_ok(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch("api.main.assistant_response")
    def test_assistant_returns_mocked_response(self, mock_assistant_response):
        mock_assistant_response.return_value = "salut"

        payload = {"user_id": "u1", "text": "bonjour"}
        response = self.client.post("/assistant", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "salut"})
        mock_assistant_response.assert_called_once_with("u1", "bonjour")


if __name__ == "__main__":
    unittest.main()
