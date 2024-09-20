import dedupe

# Define the fields dedupe will pay attention to using variable objects directly
FIELDS = [
    dedupe.variables.String('title'),
    dedupe.variables.String('authors'),
    dedupe.variables.String('doi'),
    dedupe.variables.Text('abstract'),
]

# Random seed for reproducibility in active learning
RANDOM_SEED = 42
