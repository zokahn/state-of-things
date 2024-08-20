import unittest
from unittest.mock import patch
from companion_script import create_project

class TestCompanionScript(unittest.TestCase):
    @patch('companion_script.requests.post')
    def test_create_project(self, mock_post):
        mock_post.return_value.json.return_value = {'id': 1, 'name': 'Test', 'description': 'Test Project'}
        mock_post.return_value.status_code = 200

        result = create_project('Test', 'Test Project')

        self.assertEqual(result, {'id': 1, 'name': 'Test', 'description': 'Test Project'})
        mock_post.assert_called_once_with('http://localhost:8000/projects/', json={'name': 'Test', 'description': 'Test Project'})

if __name__ == '__main__':
    unittest.main()