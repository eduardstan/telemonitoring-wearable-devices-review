from collections import defaultdict
from .base_parser import BaseParser

class NBIBParser(BaseParser):
    def parse(self):
        """Parse an NBIB file and return records as a list of dictionaries."""
        records = []
        current_record = defaultdict(str)
        current_field = None  # Track the current field for multi-line values
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            if line.startswith("PMID-"):  # Start of a new record
                if current_record:  # Save the previous record if it exists
                    current_record = self.handle_missing_fields(current_record)
                    if current_record:  # Only append valid records
                        records.append(dict(current_record))
                    current_record = defaultdict(str)
                current_field = None  # Reset the current field for a new record

            # If the line starts with a known keyword, treat it as a new field
            for field, keyword in self.keywords.items():
                if line.startswith(keyword):
                    current_field = field  # Set the current field
                    # Handle multiple authors (or other fields with multiple entries)
                    if field == 'authors':
                        current_record[field] += line.strip()[len(keyword):].strip() + '; '
                    else:
                        current_record[field] += line.strip()[len(keyword):].strip() + ' '
                    break  # No need to check further keywords for this line

            # Handle multi-line abstract or other fields with indented continuation lines
            if current_field in ['abstract', 'title', 'venue'] and line.startswith('  '):  # Indented lines continue
                current_record[current_field] += line.strip() + ' '

            # Stop appending when we encounter a non-indented line or a new keyword
            if current_field in ['abstract', 'title', 'venue'] and not line.startswith('  ') and not any(line.startswith(k) for k in self.keywords.values()):
                current_field = None  # Stop appending

        # Add the last record to the list if it exists and is valid
        if current_record:
            current_record = self.handle_missing_fields(current_record)
            if current_record:  # Only append valid records
                records.append(dict(current_record))

        # Clean up by removing trailing semicolons from the authors field and spaces from each record field
        for record in records:
            for field in record:
                # Only strip if the field is not None
                if record[field] is not None:
                    record[field] = record[field].strip('; ').strip()

        return records
