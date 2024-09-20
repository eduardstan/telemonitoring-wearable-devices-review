import os
import re
import random
import dedupe
import csv
import logging
from unidecode import unidecode
from code.config import DEDUP_FIELDS, RANDOM_SEED
from code.utils.file_utils import ensure_directory_exists, find_files_with_prefix, get_output_filename

def set_random_seed(seed):
    """Set the random seed for reproducibility."""
    random.seed(seed)

def pre_process(column):
    """Clean and normalize text data."""
    column = unidecode(column)
    column = re.sub("  +", " ", column)  # Replace multiple spaces with a single space
    column = re.sub("\n", " ", column)   # Replace newlines with a space
    column = column.strip().strip('"').strip("'").lower().strip()  # Strip unnecessary characters
    
    if not column:
        return None
    return column

def read_data(filename):
    """Read CSV data and preprocess it for dedupe."""
    data_d = {}
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            clean_row = {k: pre_process(v) for k, v in row.items()}
            data_d[i] = clean_row
    return data_d

def get_training_and_settings_files(topic):
    """Generate training and settings file paths based on the topic."""
    deduplicated_dir = "data/deduplicated/"

    # Ensure deduplicated directory exists
    ensure_directory_exists(deduplicated_dir)
    
    training_file = os.path.join(deduplicated_dir, f"{topic}_training.json")
    settings_file = os.path.join(deduplicated_dir, f"{topic}_settings.json")
    return training_file, settings_file

def find_input_file(topic):
    """Find the appropriate input file by searching for 'topic_number_records.csv'."""
    parsed_folder = "data/parsed/"
    matching_files = find_files_with_prefix(parsed_folder, topic)
    if not matching_files:
        raise FileNotFoundError(f"No file found for topic '{topic}' in 'data/parsed/' folder.")
    elif len(matching_files) > 1:
        logging.warning(f"Multiple files found for topic '{topic}'. Using the first one: {matching_files[0]}")
    return matching_files[0]

def deduplicate_data(data_d, topic):
    """Run the deduplication process using Dedupe."""
    training_file, settings_file = get_training_and_settings_files(topic)
    
    # Ensure deduplicated directory exists
    ensure_directory_exists(os.path.dirname(training_file))
    
    if os.path.exists(settings_file):
        logging.info(f"Reading from settings file {settings_file}...")
        with open(settings_file, 'rb') as sf:
            deduper = dedupe.StaticDedupe(sf)
    else:
        logging.info("Initializing new deduper...")
        deduper = dedupe.Dedupe(DEDUP_FIELDS, num_cores=1)
        deduper.prepare_training(data_d)
        
        if os.path.exists(training_file):
            logging.info(f"Loading training file {training_file}...")
            with open(training_file, 'rb') as tf:
                deduper.prepare_training(data_d, tf)
        else:
            logging.info("Starting active labeling...")
            dedupe.console_label(deduper)
            with open(training_file, 'w') as tf:
                deduper.write_training(tf)
        
        deduper.train()
        with open(settings_file, 'wb') as sf:
            deduper.write_settings(sf)
    
    # Perform deduplication
    logging.info("Clustering duplicates...")
    clustered_dupes = deduper.partition(data_d, 0.5)
    logging.info(f"# duplicate sets: {len(clustered_dupes)}")
    
    return clustered_dupes

def write_results(input_file, clustered_dupes, topic):
    """Write the deduplicated results into a CSV file."""
    num_unique_records = len(clustered_dupes)
    output_file = get_output_filename("data/deduplicated/", topic, num_unique_records)
    
    cluster_membership = {}
    for cluster_id, (records, scores) in enumerate(clustered_dupes):
        # Select the first record in each cluster
        selected_record_id = records[0]
        cluster_membership[selected_record_id] = {"Cluster ID": cluster_id, "confidence_score": scores[0]}
    
    # Write results to output file
    with open(input_file, newline='', encoding='utf-8') as f_input, open(output_file, 'w', newline='', encoding='utf-8') as f_output:
        reader = csv.DictReader(f_input)
        fieldnames = ["Cluster ID", "confidence_score"] + reader.fieldnames
        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, row in enumerate(reader):
            if i in cluster_membership:
                row.update(cluster_membership[i])
                writer.writerow(row)
    
    logging.info(f"Deduplicated results saved to {output_file} with {num_unique_records} records.")

def deduplicate_file(topic):
    """Deduplicate records for a specific topic."""
    try:
        input_file = find_input_file(topic)
        logging.info(f"Importing data from {input_file}...")
        data_d = read_data(input_file)
        
        clustered_dupes = deduplicate_data(data_d, topic)
        write_results(input_file, clustered_dupes, topic)
    except Exception as e:
        logging.error(f"Error deduplicating topic '{topic}': {e}")
