"""Utility functions for use in app.py"""
from typing import Iterable, Dict, Any


def validate_fields(
    request: Dict[str, Any],
    required_fields: Iterable[str],
    non_empty_fields: Iterable[str] = ()) -> str:
    """Return error if a request contains an invalid required fields.

    Args:
        request: Dictionary request to be validated.
        required_fields: The fields that the request must have.
        non_empty_fields: Fields that must not evaluate to bool(field)=False.

    Returns:
        An error message if the request is invalid. A blank string '' if no
        error detected.
    """

    # Validate request
    for field in required_fields:
        if field not in request:
            return f'Request missing field ({field}).'
    for field in non_empty_fields:
        if not request[field]:
            return f'Request field ({field}) must not evaluate to False.'

    return ''
