"""Different Types of Inputs to use with argonauts."""

import os
import re


class Path:
    """Path input with autocompletion."""

    def __init__(self) -> None:
        """Initialize Path input."""
        pass

    @staticmethod
    def validate(path: str) -> bool:
        """Validate the given path."""
        return os.path.exists(path)


class Password:
    """Password input with masking."""

    def __init__(self) -> None:
        """Initialize Password input."""
        pass


class Email:
    """Email input with validation."""

    def __init__(self) -> None:
        """Initialize Email input."""
        pass

    @staticmethod
    def validate(email: str) -> bool:
        """Validate the given email."""
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
