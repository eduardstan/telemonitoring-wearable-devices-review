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
- **Study Methodology**: Describe the methodology used in the study (e.g., Randomized Controlled Trial, observational study, machine learning model) if available from the abstract. If the methodology is not explicitly mentioned, state "Methodology not specified".
- **Key Findings**: Summarize the key results or findings of the study as described in the abstract. If the findings are not explicitly mentioned, state "Findings not specified".
- **Study Implications**: Identify the broader implications of the study, especially in relation to telemonitoring or wearable devices, if mentioned.

### Special Cases: 
- If the study appears to be a **systematic literature review (SLR)**, **meta-analysis**, **survey**, or any other type of **review** of existing literature, you must identify it as a **Special Case**.

### Relevance Score and Justification (0-5 scale):
Evaluate the studies based on the relevance to telemonitoring or wearable devices using the criteria below:

- **Relevance Score** (0-5 scale):
  - **0**: Telemonitoring or wearable devices are **not mentioned at all** in the title or abstract.
  - **1**: Telemonitoring or wearable devices are **briefly mentioned**, but they are clearly not the focus of the study.
  - **2**: Telemonitoring or wearable devices are **mentioned alongside other technologies or methods**, but they are not a central focus.
  - **3**: Telemonitoring or wearable devices are **moderately discussed**, but their role is **supportive or secondary** to other main topics.
  - **4**: Telemonitoring or wearable devices are **significantly discussed**, playing a **major role** in the study's objectives, but **not the sole focus**.
  - **5**: Telemonitoring or wearable devices are **the central focus** of the study, and the study **directly investigates** or addresses them.

- **Relevance Justification**: You must provide a clear explanation for the assigned **Relevance Score**, following this format strictly:
  - **Mention**: Were telemonitoring or wearable devices mentioned in the title or abstract?
    - **Yes**
    - **No**
  - **Focus**: To what extent are telemonitoring or wearable devices a focus of the study? 
    - **Briefly mentioned**
    - **Discussed alongside other technologies** 
    - **Central focus**
  - **Role**: What role do telemonitoring or wearable devices play in the study? 
    - **Minor** 
    - **Supportive** 
    - **Central**

### IMPORTANT INSTRUCTIONS:
For **both cases (special and non)**, you must output the following fields:
- `"Relevance Score": {score}`, where `{score}` is the score from 0 to 5
- `"Relevance Justification": "Mention: {Yes/No}. Focus: {Briefly mentioned/Discussed alongside other technologies/Central focus}. Role: {Minor/Supportive/Central}."`
- `"Special Case Reason":` 
  - `"Systematic review, meta-analysis, or survey (literature review)"` for special cases.
  - `"N/A"` for non-special ones.

Do not deviate from these formats. Do not add additional text or explanations outside the required format.

### Formatting Instructions:
Return your output in **strict JSON format**. Do not include any extraneous text, explanations, or markdown. Only return the JSON object using the following this structure:
{
  "Title": "...",
  "Author(s)": "...",
  "Year": "...", # Ensure all values are strings 
  "Venue": "...",
  "Study Objectives": "...",
  "Study Methodology": "...",
  "Key Findings": "...",
  "Study Implications": "...",
  "Relevance Score": "...",
  "Relevance Justification": "...",
  "Special Case Reason": "..." # Set to "N/A" if not applicable
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
    'usability': 'This search focused on the **human-computer interaction** aspects of telemonitoring systems, including **usability and user experience**.'
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
