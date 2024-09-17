import dedupe

# Define the fields dedupe will pay attention to using variable objects directly
FIELDS = [
    dedupe.variables.String('title'),
    dedupe.variables.String('authors'),
    dedupe.variables.String('doi'),
    dedupe.variables.String('venue'),
    dedupe.variables.Text('abstract'),
    dedupe.variables.String('publication_language', has_missing=True),
]

# Random seed for reproducibility in active learning
RANDOM_SEED = 42

# Input and output files
INPUT_FILE = "data/parsed/accessibility_317_records.csv"
OUTPUT_FILE = "data/deduplicated/accessibility_deduped.csv"
SETTINGS_FILE = "data/deduplicated/accessibility_dedupe_settings.json"
TRAINING_FILE = "data/deduplicated/accessibility_dedupe_training.json"
