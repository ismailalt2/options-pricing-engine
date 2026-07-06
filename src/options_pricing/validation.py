from __future__ import annotations

CALL = "call"
PUT = "put"
EUROPEAN = "european"
AMERICAN = "american"

_OPTION_TYPES = (CALL, PUT)
_EXERCISE_STYLES = (EUROPEAN, AMERICAN)


def validate_positive(name: str, value: float) -> float:
    if value is None or not (value > 0):
        raise ValueError(f"{name} must be strictly positive, got {value!r}")
    return float(value)


def validate_nonnegative(name: str, value: float) -> float:
    if value is None or value < 0:
        raise ValueError(f"{name} must be non-negative, got {value!r}")
    return float(value)


def validate_option_type(option_type: str) -> str:
    if not isinstance(option_type, str):
        raise TypeError(f"option_type must be a string, got {type(option_type).__name__}")
    normalised = option_type.strip().lower()
    if normalised not in _OPTION_TYPES:
        raise ValueError(f"option_type must be one of {_OPTION_TYPES}, got {option_type!r}")
    return normalised


def validate_exercise(exercise: str) -> str:
    if not isinstance(exercise, str):
        raise TypeError(f"exercise must be a string, got {type(exercise).__name__}")
    normalised = exercise.strip().lower()
    if normalised not in _EXERCISE_STYLES:
        raise ValueError(f"exercise must be one of {_EXERCISE_STYLES}, got {exercise!r}")
    return normalised


def validate_positive_int(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer, got {value!r}")
    return value
