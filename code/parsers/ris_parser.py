from collections import defaultdict
from .base_parser import BaseParser
from .parser_utils import extract_field_value, append_field_value
import logging

class RISParser(BaseParser):
    def parse(self):
        """Parse an RIS file and return records as a list of dictionaries."""
        records = []
        current_record = defaultdict(str)

        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split the file content by two consecutive newlines to separate records
        raw_records = content.split("\n\n")

        for raw_record in raw_records:
            lines = raw_record.splitlines()

            for line in lines:
                if line.startswith("ER"):  # End of record
                    processed_record = self.handle_missing_fields(current_record)
                    if processed_record:
                        records.append(processed_record)
                    current_record = defaultdict(str)
                    break

                # Extract field information from each line
                for field, keyword in self.keywords.items():
                    if line.startswith(keyword):
                        value = extract_field_value(line, keyword)
                        is_multiple = field == 'authors'
                        append_field_value(current_record, field, value, is_multiple)
                        break  # Move to next line after matching a keyword

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
