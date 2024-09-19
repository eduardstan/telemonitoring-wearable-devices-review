import unittest
import sys
import os

# Add the parent directory to sys.path to import modules correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.ris_parser import RISParser
from parsers.config import RIS_KEYWORDS

class TestRISParser(unittest.TestCase):
    def test_parse(self):
        selected_fields = ['title', 'authors', 'doi', 'venue', 'publication_language']
        required_fields = ['title', 'authors', 'venue']
        optional_fields = ['doi', 'publication_language']
        
        parser = RISParser('data/tests/sample.ris', selected_fields, required_fields, optional_fields, RIS_KEYWORDS)
        records = parser.parse()
        
        self.assertEqual(len(records), 27)
        self.assertIn('title', records[0])
        self.assertIn('authors', records[0])
        self.assertIn('doi', records[0])
        self.assertIn('publication_language', records[0])

if __name__ == '__main__':
    unittest.main()
