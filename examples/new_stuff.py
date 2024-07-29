"""Example of using the new argonauts API."""

import time

from argonauts import argonaut
from argonauts.inputs import Email, Password, Path


@argonaut(process_name="Please wait...")
def login(email: Email, password: Password) -> None:
    """Login with email and password."""
    time.sleep(3)
    print(f"Logged in with {email}.")


@argonaut(process_name="Loading Configurations...")
def configure(config_path: Path) -> None:
    """Configure with the given path."""
    time.sleep(3)
    print(f"Configured with {config_path}.")


if __name__ == "__main__":
    login()
    configure()
