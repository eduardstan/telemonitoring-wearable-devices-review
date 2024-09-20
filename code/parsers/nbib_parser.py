from collections import defaultdict
from .base_parser import BaseParser
from .parser_utils import extract_field_value, append_field_value
import logging

class NBIBParser(BaseParser):
    def parse(self):
        """Parse an NBIB file and return records as a list of dictionaries."""
        records = []
        current_record = defaultdict(str)
        current_field = None  # Track the current field for multi-line values

        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.rstrip()

            if line.startswith("PMID-"):  # Start of a new record
                if current_record:
                    processed_record = self.handle_missing_fields(current_record)
                    if processed_record:
                        records.append(processed_record)
                    current_record = defaultdict(str)
                current_field = None  # Reset the current field for a new record

            # Check if the line starts with any known keyword
            for field, keyword in self.keywords.items():
                if line.startswith(keyword):
                    current_field = field
                    value = extract_field_value(line, keyword)
                    is_multiple = field == 'authors'
                    append_field_value(current_record, field, value, is_multiple)
                    break  # Move to next line after matching a keyword
            else:
                # Handle multi-line continuation for specific fields
                if current_field in ['abstract', 'title', 'venue']:
                    if line.startswith('  '):  # Indented lines continue the field
                        value = line.strip()
                        append_field_value(current_record, current_field, value)
                    else:
                        current_field = None  # Stop appending if not indented or new keyword

        # Add the last record to the list if it's valid
        if current_record:
            processed_record = self.handle_missing_fields(current_record)
            if processed_record:
                records.append(processed_record)

        # Final cleanup of records
        for record in records:
            for field in record:
                if record[field] is not None:
                    record[field] = record[field].strip('; ').strip()

        return records
