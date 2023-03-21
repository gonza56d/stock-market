from typing import Any


class NotFound(Exception):
    """Raised when a requested element was not found."""

    def __init__(self, entity: str, by_what: str, by_value: Any):
        super().__init__(
            'The requested entity: '
            f'"{entity}", was not found by {by_what}: "{by_value}".'
        )
