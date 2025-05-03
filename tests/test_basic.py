"""
Basic tests for i18n-checker functionality.
"""
import os
import json
import tempfile
import unittest
from i18n_checker.checker import (
    find_files,
    extract_keys_from_json,
    extract_nested_keys,
    determine_language_from_path
)

class TestI18nChecker(unittest.TestCase):
    """Test class for i18n-checker core functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        
        # Create some test files
        self.json_path = os.path.join(self.test_dir.name, "en.json")
        self.test_json = {
            "greeting": "Hello",
            "user": {
                "name": "User name",
                "email": "Email address"
            },
            "messages": ["Message 1", "Message 2"]
        }
        
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.test_json, f)
            
    def tearDown(self):
        """Tear down test fixtures."""
        self.test_dir.cleanup()
        
    def test_find_files(self):
        """Test finding files with specific extensions."""
        # Create additional test files
        with open(os.path.join(self.test_dir.name, "test.py"), "w") as f:
            f.write("# Test Python file")
            
        with open(os.path.join(self.test_dir.name, "test.js"), "w") as f:
            f.write("// Test JavaScript file")
            
        # Test finding Python files
        py_files = find_files(self.test_dir.name, ".py")
        self.assertEqual(len(py_files), 1)
        
        # Test finding JavaScript files
        js_files = find_files(self.test_dir.name, ".js")
        self.assertEqual(len(js_files), 1)
        
        # Test finding JSON files
        json_files = find_files(self.test_dir.name, ".json")
        self.assertEqual(len(json_files), 1)
        
    def test_extract_keys_from_json(self):
        """Test extracting keys from a JSON file."""
        keys = extract_keys_from_json(self.json_path)
        expected_keys = {"greeting", "user", "user.name", "user.email", "messages"}
        self.assertEqual(keys, expected_keys)
        
    def test_extract_nested_keys(self):
        """Test extracting nested keys from a dictionary."""
        keys = extract_nested_keys(self.test_json)
        expected_keys = {"greeting", "user", "user.name", "user.email", "messages"}
        self.assertEqual(keys, expected_keys)
        
    def test_determine_language_from_path(self):
        """Test determining language from file path."""
        # Test with language in filename
        self.assertEqual(determine_language_from_path(self.json_path), "en")
        
        # Test with language in directory path
        lang_dir = os.path.join(self.test_dir.name, "fr")
        os.makedirs(lang_dir, exist_ok=True)
        fr_path = os.path.join(lang_dir, "messages.json")
        with open(fr_path, "w") as f:
            f.write("{}")
        self.assertEqual(determine_language_from_path(fr_path), "fr")
        
if __name__ == "__main__":
    unittest.main() 