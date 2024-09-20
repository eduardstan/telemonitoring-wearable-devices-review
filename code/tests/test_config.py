import unittest
from code.config import SELECTED_FIELDS, REQUIRED_FIELDS, OPTIONAL_FIELDS, RIS_KEYWORDS, NBIB_KEYWORDS

class TestConfig(unittest.TestCase):

    def test_selected_fields(self):
        """Test that selected fields are correctly defined."""
        self.assertIn('title', SELECTED_FIELDS)
        self.assertIn('authors', SELECTED_FIELDS)
        self.assertIn('doi', SELECTED_FIELDS)

    def test_ris_keywords(self):
        """Test that RIS keywords are correctly mapped."""
        self.assertIn('title', RIS_KEYWORDS)
        self.assertEqual(RIS_KEYWORDS['title'], 'TI  -')

    def test_nbib_keywords(self):
        """Test that NBIB keywords are correctly mapped."""
        self.assertIn('title', NBIB_KEYWORDS)
        self.assertEqual(NBIB_KEYWORDS['title'], 'TI  -')

if __name__ == '__main__':
    unittest.main()
