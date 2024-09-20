import os
import pandas as pd
from ris_parser import RISParser
from nbib_parser import NBIBParser
from config import RIS_KEYWORDS, NBIB_KEYWORDS, EMBASE_RIS_KEYWORDS

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
    # Handle files split by IEEE Xplore into numbered parts
    files_to_read = [f for f in os.listdir(folder_path) if f.startswith(sub_topic) or f.startswith(f"{sub_topic}_")]
    
    all_records = []
    total_parsed_records, total_skipped_records = 0, 0
    
    for file_name in files_to_read:
        file_path = os.path.join(folder_path, file_name)
        print(f"Processing file: {file_path}")
        
        try:
            parser = get_parser(file_name, database_folder, file_path, selected_fields, required_fields, optional_fields)
            file_records = parser.parse()

            # Track total records
            total_parsed_records += parser.num_parsed_records
            total_skipped_records += parser.num_skipped_records

            all_records.extend(file_records)
        
        except ValueError as e:
            print(e)  # Log unsupported formats or errors
            
    return all_records, total_parsed_records, total_skipped_records

def parse_data_from_multiple_sources(databases, sub_topics, output_file=None):
    all_records = []
    total_parsed_records, total_skipped_records = 0, 0  # Track totals
    
    # Fields for all parsers
    selected_fields = ['title', 'authors', 'doi', 'venue', 'year', 'abstract', 'publication_language']
    required_fields = ['title', 'authors', 'venue', 'doi', 'year', 'abstract']
    optional_fields = ['publication_language']
    
    for database_folder in databases:
        for sub_topic in sub_topics:
            records, parsed, skipped = parse_files_in_folder(database_folder, sub_topic, selected_fields, required_fields, optional_fields)
            all_records.extend(records)
            total_parsed_records += parsed
            total_skipped_records += skipped

    # Handle output file
    if not output_file:
        output_file = f"data/parsed/{'_'.join(sub_topics)}_{total_parsed_records}_records.csv"
    
    # Write to CSV
    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv(output_file, index=False)
        print(f"Data successfully saved to {output_file} with {total_parsed_records} valid records.")
    
    print(f"Total records processed: {total_parsed_records + total_skipped_records}")
    print(f"Total records skipped: {total_skipped_records}")

if __name__ == "__main__":
    databases = input("Enter databases (comma-separated, e.g., embase, ieee_xplore): ").split(", ")
    sub_topics = input("Enter sub-topics (comma-separated, e.g., ai methods, accessibility): ").split(", ")
    output_file = input("Enter the output CSV file path (optional, leave blank for default): ")

    # parse_data_from_multiple_sources(["embase", "ieee_xplore", "pubmed", "scopus"], sub_topics, output_file)
    parse_data_from_multiple_sources(databases, sub_topics, output_file)
