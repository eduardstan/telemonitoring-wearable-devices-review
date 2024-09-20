import os
import pandas as pd
import logging
from code.parsers.ris_parser import RISParser
from code.parsers.nbib_parser import NBIBParser
from code.config import RIS_KEYWORDS, NBIB_KEYWORDS, EMBASE_RIS_KEYWORDS

def get_parser(file_name, database_folder, file_path, selected_fields, required_fields, optional_fields):
    """Initialize the correct parser based on file format and database."""
    if file_name.endswith('.ris'):
        if database_folder.strip().lower() == 'embase':
            return RISParser(file_path, selected_fields, required_fields, optional_fields, EMBASE_RIS_KEYWORDS)
        else:
            return RISParser(file_path, selected_fields, required_fields, optional_fields, RIS_KEYWORDS)
    elif file_name.endswith('.nbib'):
        return NBIBParser(file_path, selected_fields, required_fields, optional_fields, NBIB_KEYWORDS)
    else:
        raise ValueError(f"Unsupported file format: {file_name}")

def parse_files_in_folder(database_folder, sub_topic, selected_fields, required_fields, optional_fields):
    """Parse all files in the folder that match the sub-topic and return the records."""
    folder_path = f'data/raw/{database_folder}/'
    files_to_read = [f for f in os.listdir(folder_path) if f.startswith(sub_topic) or f.startswith(f"{sub_topic}_")]
    
    all_records = []
    total_parsed_records, total_skipped_records = 0, 0
    
    for file_name in files_to_read:
        file_path = os.path.join(folder_path, file_name)
        logging.info(f"Processing file: {file_path}")
        
        try:
            parser = get_parser(file_name, database_folder, file_path, selected_fields, required_fields, optional_fields)
            file_records = parser.parse()

            # Track total records
            total_parsed_records += parser.num_parsed_records
            total_skipped_records += parser.num_skipped_records

            all_records.extend(file_records)
        
        except ValueError as e:
            logging.error(f"Error parsing file {file_name}: {e}")
            
    return all_records, total_parsed_records, total_skipped_records

def parse_data_from_multiple_sources(databases, sub_topics):
    """Parse data from multiple databases and sub-topics and save results."""
    selected_fields = ['title', 'authors', 'doi', 'venue', 'year', 'abstract', 'publication_language']
    required_fields = ['title', 'authors', 'venue', 'doi', 'year', 'abstract']
    optional_fields = ['publication_language']

    # Process each sub-topic separately
    for sub_topic in sub_topics:
        all_records = []
        total_parsed_records, total_skipped_records = 0, 0  # Track totals

        # Loop through each database
        for database_folder in databases:
            records, parsed, skipped = parse_files_in_folder(database_folder, sub_topic, selected_fields, required_fields, optional_fields)
            all_records.extend(records)
            total_parsed_records += parsed
            total_skipped_records += skipped

        # Define output file based on the repository structure
        output_file = f"data/parsed/{sub_topic}_{total_parsed_records}_records.csv"

        # Write to CSV
        if all_records:
            df = pd.DataFrame(all_records)
            df.to_csv(output_file, index=False)
            logging.info(f"Data successfully saved to {output_file} with {total_parsed_records} valid records.")

        logging.info(f"Total records processed: {total_parsed_records + total_skipped_records}")
        logging.info(f"Total records skipped: {total_skipped_records}")
