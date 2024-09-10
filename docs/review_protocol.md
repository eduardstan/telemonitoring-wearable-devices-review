### Reviewing Protocol for Systematic Literature Review on Telemonitoring and Wearable Devices

#### 1. **Objective**
The primary objective of this systematic review is to explore recent developments in telemonitoring and wearable devices in healthcare from 2020 onwards. The review focuses on:
- The role of AI methods,
- Interoperability,
- Legal frameworks and regulations,
- Communication protocols,
- Data privacy and security,
- Accessibility and usability.

This study evaluates how these technologies impact healthcare delivery and assesses the research landscape across the last few years.

#### 2. **Databases and Search Strategy**

##### Search Query
The following query was used to retrieve records from the four databases:

```plaintext
("distant monitoring" OR 
"distant patient monitoring" OR 
"distant surveillance" OR 
"distant patient surveillance" OR 
"healthcare monitoring" OR 
"health-care monitoring" OR 
"health care monitoring" OR 
"healthcare surveillance" OR 
"health-care surveillance" OR
"health care surveillance" OR 
"patient surveillance" OR 
"remote distance patient monitoring" OR 
"remote monitoring" OR 
"remote patient monitoring" OR 
"RPM" OR 
"remote distance patient surveillance" OR 
"remote surveillance" OR 
"remote patient surveillance" OR 
"telemonitoring" OR 
"tele-monitoring" OR 
"tele monitoring" OR 
"telesurveillance" OR 
"tele-surveillance" OR 
"tele surveillance") 

AND 

("bioapparatus" OR "bioapparatuses" OR 
"bio-apparatus" OR "bio-apparatuses" OR 
"bio apparatus" OR "bio apparatuses" OR 
"biodevice" OR "biodevices" OR 
"bio-device" OR "bio-devices" OR 
"bio device" OR "bio devices" OR 
"bioequipment" OR 
"bio-equipment" OR 
"bio equipment" OR 
"biosensor" OR "biosensors" OR 
"bio-sensor" OR "bio-sensors" OR
"bio sensor" OR "bio sensors" OR 
"biotechnology" OR "biotechnologies" OR 
"bio-technology" OR "bio-technologies" OR 
"bio technology" OR "bio technologies" OR 

"bodyworn apparatus" OR "bodyworn apparatuses" OR 
"body-worn apparatus" OR "body-worn apparatuses" OR 
"body worn apparatus" OR "body worn apparatuses" OR 
"bodyworn device" OR "bodyworn devices" OR 
"body-worn device" OR "body-worn devices" OR 
"body worn device" OR "body worn devices" OR 
"bodyworn equipment" OR 
"body-worn equipment" OR 
"body worn equipment" OR 
"bodyworn sensor" OR "bodyworn sensors" OR 
"body-worn sensor" OR "body-worn sensors" OR 
"body worn sensor" OR "body worn sensors" OR 
"bodyworn technology" OR "bodyworn technologies" OR 
"body-worn technology" OR "body-worn technologies" OR 
"body worn technology" OR "body worn technologies" OR 

"healthcare apparatus" OR "healthcare apparatuses" OR 
"health-care apparatus" OR "health-care apparatuses" OR 
"health care apparatus" OR "health care apparatuses" OR 
"healthcare device" OR "healthcare devices" OR 
"health-care device" OR "health-care devices" OR 
"health care device" OR "health care devices" OR 
"healthcare equipment" OR 
"health-care equipment" OR 
"health care equipment" OR 
"healthcare sensor" OR "healthcare sensors" OR 
"health-care sensor" OR "health-care sensors" OR 
"health care sensor" OR "health care sensors" OR 
"healthcare technology" OR "healthcare technologies" OR 
"health-care technology" OR "health-care technologies" OR 
"health care technology" OR "health care technologies" OR 

"medical apparatus" OR "medical apparatuses" OR 
"medical device" OR "medical devices" OR 
"medical equipment" OR 
"medical sensor" OR "medical sensors" OR 
"medical technology" OR "medical technologies" OR 

"wearable" OR "wearables" OR 
"wearable apparatus" OR "wearable apparatuses" OR 
"wearable device" OR "wearable devices" OR 
"wearable equipment" OR 
"wearable sensor" OR "wearable sensors" OR 
"wearable technology" OR "wearable technologies")
```

The review was limited to studies published from **2020 onwards**.

##### Data Download Specifications

- **PubMed**: PubMed provides data in **NBIB format**. All PubMed files were downloaded in this format, using default settings.
- **Embase**: Data was downloaded in **RIS format** using the default download options.
- **Scopus**: Scopus files were downloaded in **RIS format**, with all available information from "Citation information" and "Abstract & keywords" included.
- **IEEE Xplore**: Data was downloaded in **RIS format**, selecting "Citation and Abstract" options. IEEE Xplore limits each download to 100 records per page, so files are split into chunks (e.g., `topic_1_100_records.ris`, `topic_101_201_records.ris`, etc.).

##### Results 
We obtained the following results:
- **Embase**: 2267 records
- **IEEE Xplore**: 1213 records
- **PubMed**: 2035 records
- **Scopus**: 3393 records

#### 3. **Topic Refinement**
After the initial search, the query was refined to target specific subtopics of interest within telemonitoring and wearable devices:
- **AI Methods**: Evaluating the role of artificial intelligence in enhancing telemonitoring and decision-making.
- **Interoperability**: Exploring standards and protocols that enable different systems and devices to work together seamlessly.
- **Laws and Regulations**: Investigating the regulatory frameworks governing the development and deployment of telemonitoring and wearable devices.
- **Communication Protocols**: Examining how data transmission is handled between devices, platforms, and healthcare providers.
- **Data Privacy and Security**: Assessing mechanisms to protect sensitive patient data in telemonitoring applications.
- **Accessibility**: Ensuring that telemonitoring solutions are available and usable for all patients, including those with disabilities.
- **Usability**: Evaluating how easy and efficient these devices are for healthcare professionals and patients to use.

#### 4. **Screening Process**
- The initial screening was conducted based on each retrieved paper's **title** and **abstract**.
- Studies unrelated to healthcare or that did not focus on telemonitoring and wearable devices were excluded.
- Inclusion criteria were developed based on the study objectives and topics of interest (e.g., AI, interoperability).
- The full text of each paper that passed the initial screening was then assessed for eligibility.

#### 5. **Data Management**
- Raw records from each database were stored in the `/data/raw/` folder, organized by database and topic.
- RIS and NBIB formats were used to store bibliographic data, ensuring compatibility with reference management tools like Zotero.
- The data was then parsed and deduplicated using custom Python scripts to clean the dataset before analysis.

#### 6. **PRISMA Compliance**
This systematic review follows the PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) guidelines to ensure transparency and rigor in the review process. A PRISMA flow diagram documents the study selection process, including records retrieved, screened, and excluded.

#### 7. **Inclusion/Exclusion Criteria**
- **Inclusion Criteria**: 
  - Studies focused on telemonitoring and wearable devices in healthcare.
  - Papers published from 2020 onwards.
  - Studies that include discussions on AI, interoperability, laws and regulations, or other refined topics.
- **Exclusion Criteria**:
  - Studies not related to healthcare or outside the defined scope.
  - Papers in languages other than English (unless translations were available).
  - Studies lacking sufficient information on technology, methodology, or implementation details.

#### 8. **Expected Outcomes**
This review aims to identify key trends, challenges, and opportunities in telemonitoring and wearable devices, with an emphasis on the aforementioned topics. The findings will provide insight into the current state of research and potential future directions.
