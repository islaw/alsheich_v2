# parse_filename.py - v2.0 (Flexible Parser)

import re
from datetime import datetime

class ParsingError(Exception):
    pass

def parse_filename(filename: str) -> dict:
    """
    Parses various filename formats like:
    - 'Name With Spaces_YYYY-MM-DD.pdf'
    - 'Name-With-Hyphens YYYY-MM-D.pdf'
    - 'Name D-M-YY.pdf'
    - 'Name YYYY-M-D.pdf'
    """
    # Regex to capture the name part (non-digits) and the date part (digits and hyphens)
    # It handles both space and underscore as separators right before the date.
    match = re.match(r'(.+?)[ _](\d{1,4}[-.]\d{1,2}[-.]\d{2,4})\.pdf$', filename.strip(), re.IGNORECASE)
    
    if not match:
        raise ParsingError(f"Filename '{filename}' does not match any expected format.")
    
    # Clean up the witness name part
    witness_name = match.group(1).replace('-', ' ').strip()
    date_str = match.group(2).replace('.', '-') # Normalize date separator to hyphen
    
    # Try parsing different date formats, from most specific to least
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d-%m-%y'):
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            # Handle two-digit year ambiguity (e.g., '24' becomes 2024)
            if fmt == '%d-%m-%y' and parsed_date.year > 2030:
                 parsed_date = parsed_date.replace(year=parsed_date.year - 100)
            break
        except ValueError:
            continue
    else:
        raise ParsingError(f"Could not parse date '{date_str}' in filename '{filename}'.")

    return {'witness_name': witness_name, 'date': parsed_date.strftime('%Y-%m-%d')}