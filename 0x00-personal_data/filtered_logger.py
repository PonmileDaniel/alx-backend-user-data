#!/usr/bin/env python3
"""
A module to filter personal data fields in log messages.
"""

import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Replace occurrences of specified fields in a message with the redaction str
    """
    for field in fields:
        message = re.sub(f"(?<={field}=)[^{separator}]*", redaction, message)
    return message
