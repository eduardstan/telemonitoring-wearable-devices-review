# Telemonitoring and Wearable Devices Systematic Review (2020 Onwards)

## Overview
This repository contains resources, data, and code for a systematic review of telemonitoring and wearable devices in healthcare, focusing on studies from 2020 onwards. The review adheres to the PRISMA guidelines, ensuring transparency and robustness in the research methodology.

## Repository Structure

### 1. **/data**
This folder contains the datasets at different stages of processing:
- **/raw/**: Raw exported data from PubMed, Scopus, Embase, and IEEE Xplore. The files are organized by topic and stored in `.ris` or `.nbib` formats.
  - `example: /data/raw/embase/ai_methods_100_records.ris`
  - `example: /data/raw/pubmed/accessibility_50_records.nbib`
  
- **/parsed/**: Processed and parsed data, stored in CSV format. This is where the raw data is transformed into structured records for analysis.
  - `example: /data/parsed/ai_methods_100_records.csv`

- **/deduplicated/**: Deduplicated data, stored in CSV format. This folder contains the final cleaned data with duplicate records removed.
  - `example: /data/deduplicated/ai_methods_90_records.csv`

### 2. **/code**
This folder contains all Python scripts for parsing, deduplication, logging, and other utilities.

#### **/parsers/**
Handles the parsing of raw data from RIS and NBIB formats.
- **base_parser.py**: Abstract base class for all parsers, handling common parsing functionality.
- **ris_parser.py**: Parser specifically for RIS files, such as those exported from Scopus, Embase, or IEEE Xplore.
- **nbib_parser.py**: Parser for NBIB files, typically exported from PubMed.
- **parse.py**: Main script to handle parsing of data from multiple sources, converting them into structured CSV files.
- **parser_utils.py**: Contains utility functions for processing and cleaning parsed records, such as:
  - `extract_field_value(line, keyword)`: Extracts the field value from a line based on the keyword.
  - `append_field_value(current_record, field, value, is_multiple=False)`: Appends extracted values to the current record.

#### **/deduplication/**
Manages the deduplication of parsed records using the Dedupe library.
- **deduplicate.py**: The main deduplication script that removes duplicate records across databases.

#### **/utils/**
Provides utility scripts for logging, file handling, and other common operations.
- **logging_utils.py**: Configures and sets up logging across the repository.
- **file_utils.py**: Contains utility functions for file handling, such as ensuring directories exist and finding files with specific prefixes.

#### **/config.py**
This file stores the global configuration for the project, including the fields to be selected, required, and optional during parsing, as well as deduplication settings.

- **EMBASE_RIS_KEYWORDS**: RIS-specific keywords for parsing records from Embase.
- **RIS_KEYWORDS**: Keywords for parsing RIS records (Scopus and IEEE Xplore).
- **NBIB_KEYWORDS**: Keywords for parsing NBIB records (PubMed).
- **SELECTED_FIELDS**: Defines the fields selected during parsing (`title`, `authors`, `doi`, `venue`, `year`, etc.).
- **REQUIRED_FIELDS**: Lists required fields for valid records (`title`, `authors`, `doi`, etc.).
- **OPTIONAL_FIELDS**: Lists optional fields that are parsed but not required (`publication_language`).
- **DEDUP_FIELDS**: Specifies the fields used for deduplication (`title`, `authors`, `doi`, `abstract`).
- **RANDOM_SEED**: Sets a fixed random seed for reproducibility during active learning and deduplication.

### 3. **/notebooks**
This folder contains Jupyter notebooks for interactive data exploration and analysis.
- **parsers.ipynb**: Notebook demonstrating the parsing process for RIS and NBIB files.
- **analysis_notebook.ipynb**: A walkthrough of the data analysis and visualization of the parsed and deduplicated data.

### 4. **/docs**
This folder contains documentation related to the review process.
- **PRISMA_flowchart.png**: A visual flowchart following the PRISMA guidelines, illustrating the study selection process.
- **REVIEW_PROTOCOL.md**: Detailed documentation of the review methodology and protocol.
- **references.bib**: A BibTeX file containing references used in the review.

## How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/eduardstan/telemonitoring-wearable-devices-review.git
cd telemonitoring-wearable-devices-review
```

### 2. Set Up the Environment
Create and activate the virtual environment:
```bash
python3 -m venv telemonitoring
source telemonitoring/bin/activate
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Parse the Data
Use the provided CLI to process raw RIS and NBIB files:
```bash
python3 code/main.py parse --d embase ieee_xplore pubmed scopus --t ai_methods accessibility
```
This will parse data from the specified databases and topics, saving the parsed data into `/data/parsed/`.

### 5. Deduplicate the Data
Run the deduplication script to remove duplicate records:
```bash
python3 code/main.py deduplicate --t ai_methods accessibility
```
This will save the deduplicated data into `/data/deduplicated/`.

### 6. Analyze the Data
You can use a Jupyter notebook for step-by-step analysis:
```bash
jupyter notebook notebooks/analysis_notebook.ipynb
```

## PRISMA Compliance
This systematic review adheres to the PRISMA guidelines:
- [PRISMA Flow Diagram](docs/PRISMA_flowchart.png)
- [Review Protocol](docs/REVIEW_PROTOCOL.md)

## Data Sources
The data for this review is collected from the following databases:
- PubMed
- Scopus
- Embase
- IEEE Xplore

## License
This project is licensed under the [MIT License](LICENSE) for code, and a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) for data.

## Citation
If you use this work, please cite it as follows:
```
@misc{Stan2024,
  author = {Stan, Ionel Eduard},
  title = {Telemonitoring and Wearable Devices Survey (2020 Onwards)},
  year = {2024},
  url = {https://github.com/eduardstan/telemonitoring-wearable-devices-review}
}
```