"""Argonauts decorators."""

import argparse
import inspect
from enum import Enum
from typing import get_origin, get_args, Any, Callable
from functools import wraps
import questionary
from rich.console import Console

console = Console()

class LogBook:
    """LogBook for storing previous arguments values."""
    def __init__(self) -> None:
        self.log = argparse.Namespace()

    def __setitem__(self, key, value):
        setattr(self.log, key, value)

    def __getitem__(self, key):
        return getattr(self.log, key)
    
    def __getattribute__(self, name: str) -> Any:
        return getattr(self.log, name)
    
    def __repr__(self) -> str:
        attr_str = ", ".join([f"{k}={v}" for k, v in self.log.__dict__.items()])
        return f"LogBook({attr_str})"
    

def interactive(logbook: LogBook | None = None, include_params: list = [], process_name: str = "") -> Callable:
    """Decorator of Interactive Arguments using questionary."""
    def decorator(func: Callable) -> Callable:
        """Decorator of Interactive Arguments."""
        @wraps(func)
        def wrapper(*args: list, **kwargs: dict) -> Any: # noqa
            """Wrapper of Interactive Arguments."""
            sig = inspect.signature(func)
            params = sig.parameters
            doc_string = func.__doc__
            if doc_string:
                console.print(f"\n{doc_string}\n", style="bold")
            # Filter parameters if include_params is specified
            if include_params:
                params = {k: v for k, v in params.items() if k in include_params}

            for name, param in params.items():
                if name not in kwargs:
                    value = create_prompt(name, param)
                    if value is not None:
                        kwargs[name] = convert_value(value, param.annotation)
                    if logbook:
                        logbook[name] = kwargs[name] if name in kwargs else None
            print()
            with console.status(f"Running {func.__name__}..." if not process_name else process_name):
                output = func(*args, **kwargs)
            return output
        return wrapper
    return decorator

def create_prompt(name: str, param: inspect.Parameter) -> Any: # noqa
    """Create a prompt for the parameter."""
    annotation = param.annotation
    default = param.default if param.default != inspect.Parameter.empty else None

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        choices = [e.value for e in annotation]
        return questionary.select(
            f"Select {name}:",
            choices=choices,
            default=default.value if default and isinstance(default, Enum) else default
        ).ask()
    if get_origin(annotation) is list and issubclass(get_args(annotation)[0], Enum):
        enum_class = get_args(annotation)[0]
        choices = [e.value for e in enum_class]
        default_values = [d.value for d in default] if default and all(isinstance(d, Enum) for d in default) else default
        selected_values = questionary.checkbox(
            f"Select {name} (multiple allowed):",
            choices=choices,
            default=default_values
        ).ask()
        return [enum_class(value) for value in selected_values]
    if annotation == bool:
        return questionary.confirm(
            f"{name}?",
            default=default if default is not None else False
        ).ask()
    if annotation == str:
        print(name, default)
        return questionary.text(
            f"Enter {name}:",
            default=default if default is not None else "",
            validate=lambda text: len(text) > 0 or f"Please enter a valid {name}."
        ).ask()
    if annotation == int:
        return questionary.text(
            f"Enter {name} (integer):",
            default=str(default) if default is not None else "",
            validate=lambda text: text.isdigit() or "Please enter a valid integer."
        ).ask()
    if annotation == float:
        return questionary.float(
            f"Enter {name} (float):",
            default=default if default is not None else "",
            validate=lambda text: text.replace(".", "", 1).isdigit() or "Please enter a valid float."
        ).ask()
    
    raise ValueError(f"Unsupported type: {annotation}")
        
    
def convert_value(value: Any, annotation: Any) -> Any: # noqa
    """Convert value to the annotation type."""
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return next(e for e in annotation if e.value == value)
    elif get_origin(annotation) is list and issubclass(get_args(annotation)[0], Enum):
        enum_class = get_args(annotation)[0]
        return [enum_class(v) for v in value]
    elif annotation == int:
        return int(value)
    elif annotation == float:
        return float(value)
    else:
        return value
    

def non_interactive(func: Callable) -> Callable:
    """Decorator for non-interactive functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper