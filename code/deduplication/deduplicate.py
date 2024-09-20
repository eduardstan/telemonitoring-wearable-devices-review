import os
import dedupe
import csv
import re
import logging
import random
import numpy as np
from unidecode import unidecode
import config


def set_random_seed(seed):
    """Set the random seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)


def pre_process(column):
    """Clean and normalize text data."""
    column = unidecode(column)
    column = re.sub("  +", " ", column)  # Replace multiple spaces with a single space
    column = re.sub("\n", " ", column)   # Replace newlines with a space
    column = column.strip().strip('"').strip("'").lower().strip()  # Strip unnecessary characters
    
    if not column:
        column = None
    return column


def read_data(filename):
    """Read CSV data and preprocess it for dedupe."""
    data_d = {}
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            clean_row = [(k, pre_process(v)) for (k, v) in row.items()]
            data_d[i] = dict(clean_row)
    return data_d


def get_training_and_settings_files(topic):
    """Generate training and settings file paths based on the topic."""
    training_file = f"data/deduplicated/{topic}_training.json"
    settings_file = f"data/deduplicated/{topic}_settings.json"
    return training_file, settings_file


def find_input_file(topic):
    """Find the appropriate input file by searching for 'topic_number_records.csv'."""
    parsed_folder = "data/parsed/"
    for file_name in os.listdir(parsed_folder):
        if file_name.startswith(topic) and file_name.endswith("_records.csv"):
            return os.path.join(parsed_folder, file_name)
    
    raise FileNotFoundError(f"No file found for topic '{topic}' in the 'data/parsed/' folder.")


def deduplicate_data(data_d, topic):
    """Run the deduplication process using Dedupe."""
    training_file, settings_file = get_training_and_settings_files(topic)

    # Create the directory for deduplicated data if it doesn't exist
    os.makedirs(os.path.dirname(training_file), exist_ok=True)

    if os.path.exists(settings_file):
        print(f"Reading from settings file {settings_file}...")
        with open(settings_file, 'rb') as sf:
            deduper = dedupe.StaticDedupe(sf)
    else:
        # Initialize deduper with the fields defined in config
        deduper = dedupe.Dedupe(config.FIELDS)
        deduper.prepare_training(data_d)

        # Load or create training file
        if os.path.exists(training_file):
            with open(training_file, 'rb') as tf:
                deduper.prepare_training(data_d, tf)
        else:
            print("Starting active labeling...")
            dedupe.console_label(deduper)
            with open(training_file, 'w') as tf:
                deduper.write_training(tf)

        deduper.train()
        # Save settings for future runs
        with open(settings_file, 'wb') as sf:
            deduper.write_settings(sf)

    # Perform deduplication
    print("Clustering duplicates...")
    clustered_dupes = deduper.partition(data_d, 0.5)
    print(f"# duplicate sets: {len(clustered_dupes)}")

    return clustered_dupes


def write_results(input_file, clustered_dupes, topic):
    """Write the deduplicated results into a CSV file."""
    output_file = f"data/deduplicated/{topic}_{len(clustered_dupes)}_records.csv"
    cluster_membership = {}

    # Build the cluster membership dictionary
    for cluster_id, (records, scores) in enumerate(clustered_dupes):
        for record_id, score in zip(records, scores):
            cluster_membership[record_id] = {
                "Cluster ID": cluster_id,
                "confidence_score": score,
            }

    # Read the input file and write deduplicated records
    with open(output_file, "w", newline='') as f_output, open(input_file, newline='') as f_input:
        reader = csv.DictReader(f_input)
        fieldnames = ["Cluster ID", "confidence_score"] + reader.fieldnames
        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(reader):
            # Write only the records with unique Cluster IDs (deduplicated records)
            if i in cluster_membership:
                row.update(cluster_membership[i])
                writer.writerow(row)

    print(f"Deduplicated results saved to {output_file}")


def main():
    logging.basicConfig(level=logging.INFO)
    random_seed = config.RANDOM_SEED  # Use random seed from config
    set_random_seed(random_seed)

    # Ask for topic (to generate the dynamic input/output files)
    topic = input("Enter the topic name (e.g., ai_methods, accessibility): ").strip()

    # Find the correct input file dynamically
    input_file = find_input_file(topic)

    print(f"Importing data from {input_file}...")
    data_d = read_data(input_file)

    # Deduplication process
    clustered_dupes = deduplicate_data(data_d, topic)

    # Write deduplicated records to output
    write_results(input_file, clustered_dupes, topic)


if __name__ == "__main__":
    main()
