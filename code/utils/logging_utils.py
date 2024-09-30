import logging

def setup_logging():
    """Configure logging for the application."""
    logger = logging.getLogger()  # Get the root logger
    logger.setLevel(logging.INFO)  # Explicitly set the level to INFO

    if not logger.hasHandlers():  # Check if handlers are already set to avoid adding multiple
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(handler)
