import unittest
import logging
from code.utils.logging_utils import setup_logging

class TestLogging(unittest.TestCase):

    def test_logging_setup(self):
        """Test that logging is configured correctly."""
        setup_logging()
        logger = logging.getLogger()
        self.assertEqual(logger.level, logging.INFO)
        self.assertTrue(logger.handlers)

if __name__ == '__main__':
    unittest.main()
