import os
import pandas as pd
import logging
from code.parsers.ris_parser import RISParser
from code.parsers.nbib_parser import NBIBParser
from code.utils.file_utils import ensure_directory_exists
from code.config import RIS_KEYWORDS, NBIB_KEYWORDS, EMBASE_RIS_KEYWORDS, SELECTED_FIELDS, REQUIRED_FIELDS, OPTIONAL_FIELDS

# Use the existing logger
logger = logging.getLogger(__name__)

def get_parser(file_name, database_folder, file_path):
    """Initialize the correct parser based on file format and database."""
    if file_name.endswith('.ris'):
        if database_folder.strip().lower() == 'embase':
            return RISParser(file_path, SELECTED_FIELDS, REQUIRED_FIELDS, OPTIONAL_FIELDS, EMBASE_RIS_KEYWORDS)
        else:
            return RISParser(file_path, SELECTED_FIELDS, REQUIRED_FIELDS, OPTIONAL_FIELDS, RIS_KEYWORDS)
    elif file_name.endswith('.nbib'):
        return NBIBParser(file_path, SELECTED_FIELDS, REQUIRED_FIELDS, OPTIONAL_FIELDS, NBIB_KEYWORDS)
    else:
        raise ValueError(f"Unsupported file format: {file_name}")

def parse_folder(database_folder, sub_topic):
    """Parse all files in the folder that match the sub-topic and return the records."""
    folder_path = f'data/raw/{database_folder}/'
    files_to_read = [f for f in os.listdir(folder_path) if f.startswith(sub_topic) or f.startswith(f"{sub_topic}_")]

    all_records = []
    total_parsed_records, total_skipped_records = 0, 0

    for file_name in files_to_read:
        file_path = os.path.join(folder_path, file_name)
        logger.info(f"Processing file: {file_path}")
        
        try:
            parser = get_parser(file_name, database_folder, file_path)
            file_records = parser.parse()

            total_parsed_records += parser.num_parsed_records
            total_skipped_records += parser.num_skipped_records

            all_records.extend(file_records)

        except ValueError as e:
            logger.error(f"Error parsing file {file_name}: {e}")
            
    return all_records, total_parsed_records, total_skipped_records

def parse_sources(databases, topic):
    """Parse data from multiple databases for a single topic and save results."""
    all_records = []
    total_parsed_records, total_skipped_records = 0, 0  # Track totals

    for database_folder in databases:
        records, parsed, skipped = parse_folder(database_folder, topic)
        all_records.extend(records)
        total_parsed_records += parsed
        total_skipped_records += skipped

    # Define output file based on project structure
    output_file = f"data/parsed/{topic}_{total_parsed_records}_records.csv"

    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv(output_file, index=False)
        logger.info(f"Data successfully saved to {output_file} with {total_parsed_records} valid records.")

    logger.info(f"Total records processed: {total_parsed_records + total_skipped_records}")
    logger.info(f"Total records skipped: {total_skipped_records}")

