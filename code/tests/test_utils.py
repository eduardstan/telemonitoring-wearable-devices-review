import unittest
import os
from code.utils.file_utils import ensure_directory_exists, find_files_with_prefix

class TestUtils(unittest.TestCase):

    def setUp(self):
        """Set up test files for utils tests."""
        self.test_dir = 'test_data/raw/'  # Define test_dir here
        ensure_directory_exists(self.test_dir)
        self.test_file = os.path.join(self.test_dir, 'mock_file_records.csv')

        # Create a mock file for testing
        with open(self.test_file, 'w') as f:
            f.write('test content')

    def test_ensure_directory_exists(self):
        """Test that ensure_directory_exists creates a directory."""
        self.assertTrue(os.path.exists(self.test_dir))  # Use the defined test_dir

    def test_find_files_with_prefix(self):
        """Test that find_files_with_prefix finds the correct files."""
        matching_files = find_files_with_prefix(self.test_dir, 'mock_file')
        self.assertEqual(len(matching_files), 1)
        self.assertTrue(matching_files[0].endswith('mock_file_records.csv'))

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.test_dir):
            for f in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, f))
            os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()
