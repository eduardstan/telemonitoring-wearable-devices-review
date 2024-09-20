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
    dedupe.variables.Text('abstract'),
]

# Random seed for reproducibility in active learning and deduplication
RANDOM_SEED = 42