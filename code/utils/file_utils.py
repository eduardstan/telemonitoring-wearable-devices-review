import os

def ensure_directory_exists(path):
    """Ensure that a directory exists; if not, create it."""
    os.makedirs(path, exist_ok=True)

def find_files_with_prefix(directory, prefix, suffix="_records.csv"):
    """
    Find all files in a directory that start with a given prefix and end with a specific suffix.
    
    :param directory: Directory to search in.
    :param prefix: Prefix string to match.
    :param suffix: Suffix string to match.
    :return: List of matching file paths.
    """
    return [
        os.path.join(directory, f) 
        for f in os.listdir(directory) 
        if f.startswith(prefix) and f.endswith(suffix)
    ]

def get_output_filename(deduplicated_dir, topic, num_records):
    """
    Generate the output filename based on the topic and number of records.
    
    :param deduplicated_dir: Directory to save deduplicated files.
    :param topic: Topic name.
    :param num_records: Number of deduplicated records.
    :return: Full path to the output file.
    """
    return os.path.join(deduplicated_dir, f"{topic}_{num_records}_records.csv")
