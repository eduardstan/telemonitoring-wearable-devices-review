import unittest
import os
import pandas as pd
from code.parsers.ris_parser import RISParser
from code.parsers.nbib_parser import NBIBParser
from code.config import RIS_KEYWORDS, NBIB_KEYWORDS, EMBASE_RIS_KEYWORDS, SELECTED_FIELDS, REQUIRED_FIELDS, OPTIONAL_FIELDS
from code.utils.file_utils import ensure_directory_exists
from code.utils.logging_utils import setup_logging

class TestParsers(unittest.TestCase):

    def setUp(self):
        """Create mock files and setup necessary directories."""
        setup_logging()
        ensure_directory_exists('test_data/raw/')
        self.mock_ris_file = 'test_data/raw/mock_data.ris'
        self.mock_nbib_file = 'test_data/raw/mock_data.nbib'

        # Create mock RIS data
        ris_data = """AU  - Doe, John
TI  - Test Title
PY  - 2021
DO  - 10.1000/j.journal.2021.01.001
AB  - Test abstract for RIS
T2  - Journal of the Paper
ER  - """
        with open(self.mock_ris_file, 'w') as f:
            f.write(ris_data)

        # Create mock NBIB data
        nbib_data = """PMID- 123456
TI  - Test Title
AU  - Doe, John
DP  - 2021
LID - 10.1000/j.journal.2021.01.001
AB  - Test abstract for NBIB
JT  - Test Journal"""
        with open(self.mock_nbib_file, 'w') as f:
            f.write(nbib_data)

    def test_ris_parser(self):
        """Test RISParser parses RIS file correctly."""
        parser = RISParser(self.mock_ris_file, SELECTED_FIELDS, REQUIRED_FIELDS, OPTIONAL_FIELDS, RIS_KEYWORDS)
        records = parser.parse()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['title'], 'Test Title')
        self.assertEqual(records[0]['authors'], 'Doe, John')
        self.assertEqual(records[0]['doi'], '10.1000/j.journal.2021.01.001')

    def test_nbib_parser(self):
        """Test NBIBParser parses NBIB file correctly."""
        parser = NBIBParser(self.mock_nbib_file, SELECTED_FIELDS, REQUIRED_FIELDS, OPTIONAL_FIELDS, NBIB_KEYWORDS)
        records = parser.parse()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['title'], 'Test Title')
        self.assertEqual(records[0]['authors'], 'Doe, John')
        self.assertEqual(records[0]['doi'], '10.1000/j.journal.2021.01.001')

    def tearDown(self):
        """Clean up files after tests."""
        if os.path.exists(self.mock_ris_file):
            os.remove(self.mock_ris_file)
        if os.path.exists(self.mock_nbib_file):
            os.remove(self.mock_nbib_file)

if __name__ == '__main__':
    unittest.main()
