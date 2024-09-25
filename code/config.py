import dedupe

# Keywords mappings for different formats
EMBASE_RIS_KEYWORDS = {
    'title': 'T1  -',
    'authors': 'A1  -',
    'year': 'Y1  -',
    'doi': 'DO  -',
    'publication_language': 'LA  -',
    'publication_type': 'M3  -',
    'abstract': 'N2  -',
    'venue': 'JF  -',
}

RIS_KEYWORDS = {
    'title': 'TI  -',
    'authors': 'AU  -',
    'year': 'PY  -',
    'doi': 'DO  -',
    'publication_language': 'LA  -',
    'publication_type': 'TY  -',
    'abstract': 'AB  -',
    'venue': 'T2  -',
}

NBIB_KEYWORDS = {
    'title': 'TI  -',
    'authors': 'AU  -',
    'year': 'DP  -',
    'doi': 'LID -',
    'publication_language': 'PL  -',
    'publication_type': 'PT  -',
    'abstract': 'AB  -',
    'venue': 'JT  -',
}

# Parsing fields configuration
SELECTED_FIELDS = ['title', 'authors', 'doi', 'venue', 'year', 'abstract', 'publication_language']
REQUIRED_FIELDS = ['title', 'authors', 'venue', 'doi', 'year', 'abstract']
OPTIONAL_FIELDS = ['publication_language']

# Dedupe fields configuration
DEDUP_FIELDS = [
    dedupe.variables.String('title'),
    dedupe.variables.String('authors'),
    dedupe.variables.String('doi'),
    dedupe.variables.String('venue'),
    dedupe.variables.String('year'),
    dedupe.variables.Text('abstract'),
    dedupe.variables.String('publication_language', has_missing=True),
]

# Random seed for reproducibility in active learning and deduplication
RANDOM_SEED = 42

# System-wide system prompt
SYSTEM_PROMPT = """
Your task is to assess the relevance of research papers based solely on their title and abstract, following the guidelines in the data extraction form below.

### Data Extraction Form:
- **Title**: Provided by the user.
- **Author(s)**: Provided by the user.
- **Year**: Provided by the user.
- **Venue**: Provided by the user.
- **Study Objectives**: Summarize the primary objectives or research questions of the study, based on the abstract.
- **Study Methodology**: Describe the methodology used in the study (e.g., Randomized Controlled Trial, observational study, machine learning model) if available from the abstract. If the methodology is not explicitly mentioned, state "Methodology not specified."
- **Key Findings**: Summarize the key results or findings of the study as described in the abstract.
- **Study Implications**: Identify the broader implications of the study, especially in relation to telemonitoring or wearable devices, if mentioned.
- **Relevance to Review** (0-3 scale):
  - **0**: Not relevant to telemonitoring or wearable devices.
  - **1**: Slightly relevant (mentions telemonitoring or wearable devices but does not focus on them).
  - **2**: Moderately relevant (addresses telemonitoring or wearable devices but not central to the study).
  - **3**: Highly relevant (telemonitoring or wearable devices are the central focus of the study).

For the **Relevance to Review** score, justify your score in words and use the following format:  
`{score} ({justification})`, where **{score}** is a number from 0 to 3, and **{justification}** explains the reasoning behind your score.

### Formatting Instructions:
- Provide the output in **JSON format** following this structure:
{
  "Title": "...",
  "Author(s)": "...",
  "Year": "...",
  "Venue": "...",
  "Study Objectives": "...",
  "Study Methodology": "...",
  "Key Findings": "...",
  "Study Implications": "...",
  "Relevance to Review": "..."
}
"""

# Topic-specific descriptions
TOPIC_DESCRIPTIONS = {
    'accessibility': 'This search addressed **accessibility** in telemonitoring systems, with a focus on ensuring usability for diverse populations.',
    'ai_methods': 'This search aimed to capture studies focusing on **artificial intelligence and machine learning** applications in telemonitoring.',
    'communication_protocols': 'This search examined the underlying **communication protocols** used for data transmission in telemonitoring systems.',
    'data_security_and_privacy': 'This search focused on **data protection mechanisms and privacy** challenges in telemonitoring systems.',
    'interoperability': 'This search explored how telemonitoring devices and systems can **interoperate** within broader healthcare infrastructures.',
    'laws_and_regulations': 'This search focused on identifying **legal and regulatory frameworks** relevant to telemonitoring and wearable devices.',
    'usability': 'This search focused on the **human-computer interactio**n aspects of telemonitoring systems, including **usability and user experience**.'
}

# Function to generate user prompt dynamically
def generate_user_prompt(row, topic_description):
    return f"""
    Title: {row['title']}
    Authors: {row['authors']}
    Year: {row['year']}
    Venue: {row['venue']}
    Topic: {topic_description}
    
    Based on this information, provide information using the data extraction form.
    """
