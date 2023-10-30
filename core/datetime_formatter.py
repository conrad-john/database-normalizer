import re

def is_serialized_date(input_string) -> bool:
    # Try to match ISO 8601 format (e.g., 2023-10-29T15:30:00)
    iso8601_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?'

    # Try to match Unix timestamp (integer or float)
    unix_timestamp_pattern = r'\d+(\.\d+)?'

    # Try to match mm/dd/yyyy format (e.g., 6/15/2023)
    mm_dd_yyyy_pattern = r'\d{1,2}/\d{1,2}/\d{4}'

    # Try to match any of the above patterns
    patterns = [iso8601_pattern, unix_timestamp_pattern, mm_dd_yyyy_pattern]

    for pattern in patterns:
        if re.match(pattern, input_string):
            return True

    return False
