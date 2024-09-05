# Telemonitoring and Wearable Devices Systematic Review (2020 Onwards)

## Overview
This repository contains resources, data, and code for a systematic review of telemonitoring and wearable devices in healthcare, focusing on studies from 2020 onwards. The review follows the PRISMA guidelines to ensure a robust and transparent methodology.

## Repository Structure
- **/data**: Contains the raw and cleaned datasets from the literature search.
  - `/raw`: Raw exported data from PubMed, Scopus, Embase, and IEEE Xplore.
  - `/cleaned`: Data after deduplication.
  
- **/code**: Python scripts for processing and analyzing the datasets.
  - `deduplication.py`: Script for removing duplicate records using Dedupe.
  - `analysis.py`: Script for analyzing the data.
  
- **/notebooks**: Jupyter notebooks for reproducing the analysis.
  - `analysis_notebook.ipynb`: Walkthrough of the analysis and data visualization.

- **/docs**: Supporting documents related to the review process.
  - `PRISMA_flowchart.png`: PRISMA flowchart showing the study selection process.
  - `review_protocol.md`: Detailed protocol outlining the methodology.
  - `references.bib`: Bibliographic references in BibTeX format.

## How to Use
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eduardstan/telemonitoring-wearable-devices-review.git
   cd telemonitoring-wearable-devices-review
   ```

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Deduplicate the Data**:
   Run the deduplication script to clean the dataset:
   ```bash
   python code/deduplication.py
   ```

4. **Run the Analysis**:
   Perform the analysis using the following command:
   ```bash
   python code/analysis.py
   ```

5. **Reproduce the Analysis**:
   Open the Jupyter notebook to see the step-by-step analysis and results:
   ```bash
   jupyter notebook notebooks/analysis_notebook.ipynb
   ```

## PRISMA Compliance
This systematic review adheres to the PRISMA guidelines:
- [PRISMA Flow Diagram](docs/PRISMA_flowchart.png)
- [Review Protocol](docs/review_protocol.md)

## Data Sources
Data for this review were collected from four databases:
- PubMed
- Scopus
- Embase
- IEEE Xplore

## License
This project is licensed under the [MIT License](LICENSE) for code and a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) for data.

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
