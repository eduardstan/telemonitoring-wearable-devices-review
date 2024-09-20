def extract_field_value(line, keyword):
    """
    Extracts the value from the line based on the keyword.

    :param line: The line containing the field.
    :param keyword: The keyword to identify the field.
    :return: Extracted field value.
    """
    return line.strip()[len(keyword):].strip()

def append_field_value(current_record, field, value, is_multiple=False):
    """
    Appends the extracted value to the current record's field.

    :param current_record: The current record being processed.
    :param field: The field name.
    :param value: The extracted value.
    :param is_multiple: Whether the field can have multiple entries (e.g., authors).
    """
    if is_multiple:
        current_record[field] += value + '; '
    else:
        current_record[field] += value + ' '
