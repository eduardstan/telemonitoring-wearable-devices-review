import unittest
import sys
import os

# Add the parent directory to sys.path to import modules correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.nbib_parser import NBIBParser
from parsers.config import NBIB_KEYWORDS

class TestRISParser(unittest.TestCase):
    def test_parse(self):
        selected_fields = ['title', 'authors', 'doi', 'venue', 'publication_language']
        required_fields = ['title', 'authors', 'venue']
        optional_fields = ['doi', 'publication_language']
        
        parser = NBIBParser('data/tests/sample.nbib', selected_fields, required_fields, optional_fields, NBIB_KEYWORDS)
        records = parser.parse()
        
        self.assertEqual(len(records), 19)
        self.assertIn('title', records[0])
        self.assertIn('authors', records[0])
        self.assertIn('doi', records[0])
        self.assertIn('publication_language', records[0])

if __name__ == '__main__':
    unittest.main()
