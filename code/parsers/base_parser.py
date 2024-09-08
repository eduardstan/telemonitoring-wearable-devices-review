from abc import ABC, abstractmethod

class BaseParser(ABC):
    """Abstract base class for all parsers."""

    def __init__(self, file_path, selected_fields, required_fields, optional_fields, keyword_mapping):
        """
        :param file_path: Path to the file to be parsed.
        :param selected_fields: List of fields to parse.
        :param required_fields: List of required fields.
        :param optional_fields: List of optional fields.
        :param keyword_mapping: Dictionary mapping internal field names to RIS or NBIB tags.
        """
        self.file_path = file_path
        self.selected_fields = selected_fields
        self.required_fields = required_fields
        self.optional_fields = optional_fields
        self.keywords = {field: keyword_mapping[field] for field in selected_fields if field in keyword_mapping}

    def handle_missing_fields(self, record):
        """
        Ensure missing required fields raise an error.
        Optional fields are set to None if missing.
        """
        for field in self.required_fields:
            if field not in record or not record[field]:
                print(f"Missing required field: {field}\nRecord content: {record}")
                raise ValueError(f"Missing required field: {field}")
        
        for field in self.optional_fields:
            if field not in record or not record[field]:
                record[field] = None
        
        return record
    
    @abstractmethod
    def parse(self):
        """Parse the given file and return a list of records."""
        pass