from typing import List


def signal_to_string(signal: List[int]) -> str:
    """
    Convert a list of integers to a comma-separated string
    :param signal: List of integers representing the signal of a lead
    """
    return ",".join(map(str, signal))


def string_to_signal(signal_str: str) -> List[int]:
    """
    Convert a comma-separated string to a list of integers
    :param signal_str: Comma-separated string representing the signal of a lead
    """
    return list(map(int, signal_str.split(",")))
