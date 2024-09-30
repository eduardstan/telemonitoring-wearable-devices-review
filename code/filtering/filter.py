import logging
from openai import OpenAI
import pandas as pd
import os
from code.utils.file_utils import ensure_directory_exists, find_files_with_prefix
from code.config import SYSTEM_PROMPT, TOPIC_DESCRIPTIONS, generate_user_prompt
from dotenv import load_dotenv
import csv
import json

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Use the existing logger
logger = logging.getLogger(__name__)

def process_record(row, topic):
    """
    Process a record by passing its data to GPT for extraction based on the data extraction form.
    """
    # Fetch the topic description from config
    topic_description = TOPIC_DESCRIPTIONS.get(topic, "No specific topic description provided.")
    
    # Generate user prompt using row data and topic description
    user_prompt = generate_user_prompt(row, topic_description)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    extracted_info = response.choices[0].message.content
    
    return extracted_info

def parse_extracted_info(extracted_info):
    """
    Parses the JSON extracted information from GPT into a dictionary.
    """

    # Remove potential markdown-like backticks or other extraneous characters around the JSON
    extracted_info = extracted_info.strip().strip("```json").strip("```").strip()

    try:
        data = json.loads(extracted_info)
    except json.JSONDecodeError as e:
        logger.error("JSON decoding error: %s", e)
        logger.error("Extracted info was: %s", extracted_info)
        raise

    return data

def append_to_csv(output_file, data, write_headers=False):
    """
    Appends a row to the CSV file. If the file does not exist, it creates the file and adds headers.
    """
    # Extract the headers dynamically from the dictionary keys
    headers = list(data.keys())

    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)

        if write_headers:
            # If writing for the first time, write headers
            writer.writeheader()

        # Append the row data
        writer.writerow(data)

def process_topic(topic):
    """
    Processes all records for a given topic by reading from the deduplicated file and
    appending the filtered results to a CSV file.
    """
    # Find the deduplicated file for the topic
    dedup_dir = 'data/deduplicated/'
    files = find_files_with_prefix(dedup_dir, topic)
    if not files:
        logger.warning(f"No deduplicated files found for topic: {topic}")
        return

    # Expecting only one file for the topic
    file = files[0]
    logger.info(f"Processing file: {file}")

    # Read the deduplicated file
    df = pd.read_csv(file)

    output_dir = 'data/filtered/'
    ensure_directory_exists(output_dir)
    output_file = os.path.join(output_dir, f"{topic}_filtered_records.csv")

    write_headers = True  # First iteration should write headers

    for _, row in df.iterrows():
        # Process the record with GPT
        extracted_info = process_record(row, topic)

        # Parse the extracted info from JSON
        data = parse_extracted_info(extracted_info)

        # Append the extracted info to the CSV, writing headers only once
        append_to_csv(output_file, data, write_headers)
        write_headers = False  # Disable headers after the first row

    logger.info(f"Processed {len(df)} records for {topic} and saved to {output_file}.")
