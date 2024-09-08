from collections import defaultdict
from .base_parser import BaseParser

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
            # Process each record line by line
            lines = raw_record.splitlines()

            for line in lines:
                if line.startswith("ER"):  # End of record
                    current_record = self.handle_missing_fields(current_record)
                    records.append(dict(current_record))
                    current_record = defaultdict(str)  # Reset for the next record
                    break

                # Extract field information from each line
                for field, keyword in self.keywords.items():
                    if line.startswith(keyword):
                        # Append the value and separate multiple values with a semicolon
                        current_record[field] += line.strip()[len(keyword):].strip() + '; '

        # Add the last record to the list if it's not empty
        if current_record:
            current_record = self.handle_missing_fields(current_record)
            records.append(dict(current_record))

        # Remove trailing semicolon and space from each record field
        for record in records:
            for field in record:
                # Only strip if the field is not None
                if record[field] is not None:
                    record[field] = record[field].strip('; ').strip()
        
        return records