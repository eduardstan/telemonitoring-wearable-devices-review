from abc import ABC, abstractmethod

class BaseParser(ABC):
    """Abstract base class for all parsers."""

    def __init__(self, file_path, selected_fields, required_fields, optional_fields, keywords_mapping):
        """
        :param file_path: Path to the file to be parsed.
        :param selected_fields: List of fields to parse.
        :param required_fields: List of required fields.
        :param optional_fields: List of optional fields.
        :param keywords_mapping: Dictionary mapping internal field names to RIS or NBIB tags.
        """
        self.file_path = file_path
        self.selected_fields = selected_fields
        self.required_fields = required_fields
        self.optional_fields = optional_fields
        self.keywords = {field: keywords_mapping[field] for field in selected_fields if field in keywords_mapping}
        self.num_parsed_records = 0
        self.num_skipped_records = 0

    def clean_field(self, field_value):
        """Cleans up a field by removing trailing semicolons, commas, extra spaces, and unnecessary quotes."""
        return field_value.strip('; ').strip('"').strip(",").strip()

    def handle_missing_fields(self, record):
        """
        Ensure missing required fields cause the record to be skipped.
        Optional fields are set to None if missing.
        """
        for field in self.required_fields:
            if field not in record or not record[field].strip():
                print(f"Warning: Skipping record due to missing required field '{field}'.")
                print(f"File path: {self.file_path}\nRecord content: {record}\n")
                self.num_skipped_records += 1
                return None  # Return None if required fields are missing
        
        # Handle optional fields
        for field in self.optional_fields:
            if field not in record or not record[field].strip():
                record[field] = None

        # Clean up authors and other fields
        for field in record:
            if record[field]:
                record[field] = self.clean_field(record[field])
        
        self.num_parsed_records += 1
        return record
    
    @abstractmethod
    def parse(self):
        """Parse the given file and return a list of records."""
        pass
