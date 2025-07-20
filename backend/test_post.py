import os
import unittest
from unittest.mock import patch, MagicMock
from routes.gemini.post import save_gemini_results

USE_REAL_API = os.environ.get("USE_REAL_API", "0") == "1"

class TestSaveGeminiResults(unittest.TestCase):
    def setUp(self):
        self.itinerary_json = {
            "day_1": {
                "morning": [
                    {
                        "name": "Golden Gate Bridge",
                        "description": "Walk across the iconic bridge.",
                        "location": "Golden Gate Bridge, San Francisco, CA",
                        "start_time": "09:00",
                        "end_time": "10:30",
                        "price": 0
                    }
                ],
                "afternoon": [
                    {
                        "name": "Fisherman's Wharf",
                        "description": "Enjoy seafood and street performers.",
                        "location": "Fisherman's Wharf, San Francisco, CA",
                        "start_time": "12:00",
                        "end_time": "13:30",
                        "price": 25
                    }
                ],
                "evening": [
                    {
                        "name": "Alcatraz Island Tour",
                        "description": "Tour the historic prison island.",
                        "location": "Alcatraz Island, San Francisco, CA",
                        "start_time": "18:00",
                        "end_time": "20:00",
                        "price": 45
                    }
                ]
            },
            "day_2": {
                "morning": [
                    {
                        "name": "Golden Gate Park",
                        "description": "Relax in the park and visit museums.",
                        "location": "Golden Gate Park, San Francisco, CA",
                        "start_time": "09:30",
                        "end_time": "11:30",
                        "price": 0
                    }
                ],
                "afternoon": [
                    {
                        "name": "Chinatown Lunch",
                        "description": "Sample dim sum in Chinatown.",
                        "location": "Chinatown, San Francisco, CA",
                        "start_time": "12:30",
                        "end_time": "14:00",
                        "price": 20
                    }
                ],
                "evening": [
                    {
                        "name": "Cable Car Ride",
                        "description": "Ride the famous San Francisco cable cars.",
                        "location": "Powell St, San Francisco, CA",
                        "start_time": "19:00",
                        "end_time": "20:00",
                        "price": 8
                    }
                ]
            }
        }
        self.user_id = "60d5ec49f8d2e4a1b8c8b456"
        self.location = "San Francisco"
        self.start_date = "2024-06-01"
        self.end_date = "2024-06-02"
        self.trip_name = "Test Gemini Trip"
        # Use /api for mock, but root for real
        self.base_url = "http://localhost:8000" if USE_REAL_API else "http://localhost:8000/api"

    def run_save_gemini_results(self):
        return save_gemini_results(
            itinerary_json=self.itinerary_json,
            user_id=self.user_id,
            location=self.location,
            start_date=self.start_date,
            end_date=self.end_date,
            trip_name=self.trip_name,
            base_url=self.base_url
        )

    @unittest.skipIf(USE_REAL_API, "Skipping mock test when running real API integration test.")
    @patch("routes.gemini.post.requests.post")
    def test_save_gemini_results_mocked(self, mock_post):
        # Mock /activities response
        def side_effect(url, json):
            mock_resp = MagicMock()
            if url.endswith("/events"):
                mock_resp.status_code = 201
                mock_resp.json.return_value = {"_id": f"activity_{json['name'].replace(' ', '_')}"}
            elif url.endswith("/itineraries"):
                mock_resp.status_code = 201
                mock_resp.json.return_value = {"_id": "itinerary_123"}
            else:
                mock_resp.status_code = 404
                mock_resp.json.return_value = {}
            return mock_resp
        mock_post.side_effect = side_effect

        result = self.run_save_gemini_results()
        self.assertEqual(len(result["activity_ids"]), 6)
        self.assertEqual(result["itinerary_id"], "itinerary_123")
        activity_calls = [call for call in mock_post.call_args_list if call[0][0].endswith("/events")]
        itinerary_calls = [call for call in mock_post.call_args_list if call[0][0].endswith("/itineraries")]
        self.assertEqual(len(activity_calls), 6)
        self.assertEqual(len(itinerary_calls), 1)

    @unittest.skipUnless(USE_REAL_API, "Run this test with USE_REAL_API=1 to test real backend integration.")
    def test_save_gemini_results_real(self):
        result = self.run_save_gemini_results()
        print("\n=== Real API Test Result ===")
        print(result)
        self.assertEqual(len(result["activity_ids"]), 6)
        self.assertIsNotNone(result["itinerary_id"])

if __name__ == "__main__":
    unittest.main() 