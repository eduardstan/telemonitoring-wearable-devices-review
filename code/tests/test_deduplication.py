import unittest
import os
import logging
from code.deduplication.deduplicate import deduplicate_file, read_data
from code.utils.file_utils import ensure_directory_exists
from code.utils.logging_utils import setup_logging

class TestDeduplication(unittest.TestCase):

    def setUp(self):
        """Set up mock data for deduplication."""
        setup_logging()
        ensure_directory_exists('data/parsed/')
        ensure_directory_exists('data/deduplicated/')
        self.mock_parsed_file = 'data/parsed/mock_data_2_records.csv'
        
        # Create mock CSV data
        csv_data = """title,authors,doi,abstract,venue
        Test Title,Doe John,10.1000/j.journal.2021.01.001,Test abstract,Test Journal
        Test Title,Doe Jane,10.1000/j.journal.2021.01.001,Test abstract,Test Journal"""
        
        with open(self.mock_parsed_file, 'w') as f:
            f.write(csv_data)

    def test_read_data(self):
        """Test that CSV data is read and preprocessed correctly."""
        data = read_data(self.mock_parsed_file)
        logging.info(f"Read data: {data}")
        self.assertEqual(len(data), 2)
        self.assertIn('title', data[0])
        self.assertEqual(data[0]['title'], 'test title')

    def test_deduplicate_file(self):
        """Test deduplication process on mock data."""
        try:
            logging.info("Running deduplication on mock_data")
            deduplicate_file('mock_data')
        except Exception as e:
            logging.error(f"Deduplication failed: {e}")
        
        self.assertTrue(os.path.exists('data/deduplicated/mock_data_1_records.csv'))

    def tearDown(self):
        """Clean up files after tests."""
        if os.path.exists(self.mock_parsed_file):
            os.remove(self.mock_parsed_file)
        dedup_file = 'data/deduplicated/mock_data_1_records.csv'
        if os.path.exists(dedup_file):
            os.remove(dedup_file)

if __name__ == '__main__':
    unittest.main()
