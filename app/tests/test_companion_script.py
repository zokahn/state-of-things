
import unittest
from unittest.mock import patch
import sys
import os

# Add the directory containing the script to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.project_notes_client import create_project, list_projects

class TestProjectNotesClient(unittest.TestCase):
    @patch('scripts.project_notes_client.requests.post')
    def test_create_project(self, mock_post):
        mock_post.return_value.json.return_value = {"id": 1, "name": "Test Project", "description": "This is a test project"}
        mock_post.return_value.status_code = 200
        
        result = create_project("Test Project", "This is a test project")
        self.assertEqual(result["name"], "Test Project")
        self.assertEqual(result["description"], "This is a test project")

    @patch('scripts.project_notes_client.requests.get')
    def test_list_projects(self, mock_get):
        mock_get.return_value.json.return_value = [{"id": 1, "name": "Test Project", "description": "This is a test project"}]
        mock_get.return_value.status_code = 200
        
        result = list_projects()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test Project")

# Add more tests for other functions
