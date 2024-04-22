import re


def camel_to_snake_case(word: str) -> str:
    """
    Convert a camel case string to snake case.
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", word)
    word = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", word)
    word = word.replace("-", "_")
    return word.lower()
