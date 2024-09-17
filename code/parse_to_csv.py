import os
import pandas as pd
from parsers.ris_parser import RISParser
from parsers.nbib_parser import NBIBParser
from parsers.keywords_mapping import RIS_KEYWORDS, NBIB_KEYWORDS, EMBASE_RIS_KEYWORDS

def parse_data_from_multiple_sources(databases, sub_topics, output_file=None):
    all_records = []
    total_parsed_records = 0  # To track the total number of valid records
    total_skipped_records = 0  # To track the total number of skipped records

    # Specify the fields for all parsers to ensure consistency
    selected_fields = ['title', 'authors', 'doi', 'venue', 'abstract', 'publication_language']
    required_fields = ['title', 'authors', 'venue', 'doi', 'abstract']
    optional_fields = ['publication_language']

    for database_folder in databases:
        for sub_topic in sub_topics:
            folder_path = f'data/raw/{database_folder}/'
            files_to_read = [f for f in os.listdir(folder_path) if f.startswith(sub_topic)]

            for file_name in files_to_read:
                file_path = os.path.join(folder_path, file_name)
                print(f"Processing file: {file_path}")
                
                # Use the correct parser for RIS or NBIB format
                if file_name.endswith('.ris'):
                    # Check if the database is Scopus, and use the appropriate keyword mapping
                    if database_folder.strip().lower() == 'embase':
                        parser = RISParser(file_path, 
                                           selected_fields=selected_fields,
                                           required_fields=required_fields, 
                                           optional_fields=optional_fields, 
                                           keywords_mapping=EMBASE_RIS_KEYWORDS)
                    else:
                        parser = RISParser(file_path, 
                                           selected_fields=selected_fields,
                                           required_fields=required_fields, 
                                           optional_fields=optional_fields, 
                                           keywords_mapping=RIS_KEYWORDS)
                
                elif file_name.endswith('.nbib'):
                    parser = NBIBParser(file_path, 
                                        selected_fields=selected_fields,
                                        required_fields=required_fields, 
                                        optional_fields=optional_fields, 
                                        keywords_mapping=NBIB_KEYWORDS)
                else:
                    print(f"Unsupported file format: {file_name}")
                    continue

                # Parse the file
                file_records = parser.parse()

                # Increment counts from parser object
                total_parsed_records += parser.num_parsed_records
                total_skipped_records += parser.num_skipped_records

                # Append valid records
                all_records.extend(file_records)

    # Output file name
    if not output_file:
        total_valid_records = len(all_records)
        output_file = f"data/parsed/{'_'.join(sub_topics)}_{total_valid_records}_records.csv"
    

    # Convert records to DataFrame and write to CSV
    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv(output_file, index=False)
        print(f"Data successfully saved to {output_file} with {total_parsed_records} valid records.")
    
    print(f"Total records processed: {total_parsed_records + total_skipped_records}")
    print(f"Total records skipped: {total_skipped_records}")

if __name__ == "__main__":
    databases = input("Enter databases (comma-separated, e.g., embase, ieee_explore): ").split(", ")
    sub_topics = input("Enter sub-topics (comma-separated, e.g., ai methods, accessibility): ").split(", ")
    output_file = input("Enter the output CSV file path (optional, leave blank for default): ")

    parse_data_from_multiple_sources(databases, sub_topics, output_file)
