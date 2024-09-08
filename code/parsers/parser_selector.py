from .ris_parser import RISParser
from .nbib_parser import NBIBParser

def get_parser(file_path):
    """Return the appropriate parser based on the file extension."""
    if file_path.endswith('.ris'):
        return RISParser(file_path)
    elif file_path.endswith('.nbib'):
        return NBIBParser(file_path)
    else:
        raise ValueError(f"Unsupported file format for file: {file_path}")