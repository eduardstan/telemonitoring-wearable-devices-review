from openai import OpenAI
import pandas as pd
import os
from code.utils.file_utils import ensure_directory_exists, find_files_with_prefix
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Define the system prompt (expanded with your macro-query context)
SYSTEM_PROMPT = """
You are an expert researcher conducting a systematic literature review on telemonitoring and wearable devices in healthcare, focusing on AI methods, data privacy, usability, interoperability, and legal regulations.

Your task is to assess the relevance of research papers based only on their title and abstract, using the following data extraction form:

Data Extraction Form:
1. Study Citation:
   - Author(s): Extracted from the data.
   - Year: Extracted from the data.
   - Title: Extracted from the data.
   - Venue: Extracted from the data.
2. Study Objectives: Summarize the objectives of the study.
3. Study Methodology: Mention the methodology (if available) from the abstract.
4. Key Findings: Summarize the key findings of the study from the abstract.
5. Study Implications: Summarize the study implications if mentioned.
6. Relevance to Review (0-3 scale):
   - 0: Not relevant to telemonitoring or wearable devices.
   - 1: Slightly relevant.
   - 2: Moderately relevant.
   - 3: Highly relevant.
   
Provide your output based on this form.
"""

def process_record_with_gpt4(title, abstract, topic):
    user_prompt = f"""
    Title: "{title}"
    Abstract: "{abstract}"

    Topic: {topic}. Based on this title and abstract, provide information using the data extraction form.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    return response.choices[0].message.content

def process_topic(topic):
    # Find the latest deduplicated file for the topic
    dedup_dir = 'data/deduplicated/'
    file = find_files_with_prefix(dedup_dir, topic)
    if not file:
        print(f"No deduplicated files found for topic: {topic}")
        return

    # Since we expect only one file, take the first one
    file = file[0]

    print(f"Processing file: {file}")
    
    # Read the deduplicated file
    df = pd.read_csv(file)

    output_data = []

    for _, row in df.iterrows():
        title = row['title']
        abstract = row['abstract']
        
        # Process the title and abstract with GPT-4
        extracted_info = process_record_with_gpt4(title, abstract, topic)
        
        # Add the processed data to output
        output_data.append({
            "Cluster ID": row["Cluster ID"],
            "Authors": row['authors'],
            "Year": row['year'],
            "Title": title,
            "Venue": row['venue'],
            "Extracted Information": extracted_info
        })

    # Save the output to a new file
    output_dir = 'data/filtered/'
    output_file = os.path.join(output_dir, f"{topic}_filtered_records.csv")
    ensure_directory_exists(output_dir)
    pd.DataFrame(output_data).to_csv(output_file, index=False)
    print(f"Processed {len(output_data)} records for {topic} and saved to {output_file}.")
