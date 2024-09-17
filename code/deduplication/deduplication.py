import os
import dedupe
import csv
import re
import logging
import random
import numpy as np
from unidecode import unidecode
import dedupe_config as config


def set_random_seed(seed):
    """Set random seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)


def pre_process(column):
    """Pre-process data by normalizing and cleaning."""
    column = unidecode(column)
    column = re.sub("  +", " ", column)
    column = re.sub("\n", " ", column)
    column = column.strip().strip('"').strip("'").lower().strip()
    
    if not column:
        column = None
    return column


def read_data(filename):
    """Read CSV data into a dictionary suitable for dedupe."""
    data_d = {}
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            clean_row = [(k, pre_process(v)) for (k, v) in row.items()]
            data_d[i] = dict(clean_row)
    return data_d


def deduplicate_data(data_d):
    """Run the deduplication process."""
    if not os.path.exists(os.path.dirname(config.TRAINING_FILE)):
        os.makedirs(os.path.dirname(config.TRAINING_FILE))

    if os.path.exists(config.SETTINGS_FILE):
        print(f"Reading from settings file {config.SETTINGS_FILE}...")
        with open(config.SETTINGS_FILE, 'rb') as sf:
            deduper = dedupe.StaticDedupe(sf)
    else:
        # Initialize deduper with the defined fields
        deduper = dedupe.Dedupe(config.FIELDS) 
        deduper.prepare_training(data_d)

        if os.path.exists(config.TRAINING_FILE):
            with open(config.TRAINING_FILE, 'rb') as tf:
                deduper.prepare_training(data_d, tf)
        else:
            print("Starting active labeling...")
            dedupe.console_label(deduper)
            
            # Save the training data to the specified file
            with open(config.TRAINING_FILE, 'w') as tf:
                deduper.write_training(tf)

        deduper.train()

        # Save settings for future runs
        with open(config.SETTINGS_FILE, 'wb') as sf:
            deduper.write_settings(sf)

    # Perform deduplication
    print("Clustering duplicates...")
    clustered_dupes = deduper.partition(data_d, 0.5)

    print(f"# duplicate sets: {len(clustered_dupes)}")

    return clustered_dupes


def write_results(input_file, clustered_dupes, output_file):
    """Write the deduplicated results into a CSV."""
    cluster_membership = {}
    for cluster_id, (records, scores) in enumerate(clustered_dupes):
        for record_id, score in zip(records, scores):
            cluster_membership[record_id] = {
                "Cluster ID": cluster_id,
                "confidence_score": score,
            }

    with open(output_file, "w", newline='') as f_output, open(input_file, newline='') as f_input:
        reader = csv.DictReader(f_input)
        fieldnames = ["Cluster ID", "confidence_score"] + reader.fieldnames
        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(reader):
            row.update(cluster_membership.get(i, {"Cluster ID": None, "confidence_score": None}))
            writer.writerow(row)


def main():
    logging.basicConfig(level=logging.INFO)

    # Set the random seed for reproducibility
    set_random_seed(config.RANDOM_SEED)
    
    print("Importing data...")
    data_d = read_data(config.INPUT_FILE)
    
    deduper = deduplicate_data(data_d)
    
    write_results(config.INPUT_FILE, deduper, config.OUTPUT_FILE)


if __name__ == "__main__":
    main()
