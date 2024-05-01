import re
from typing import Any

from pydantic._internal._model_construction import ModelMetaclass


def camel_to_snake_case(word: str) -> str:
    """
    Convert a camel case string to snake case.
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", word)
    word = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", word)
    word = word.replace("-", "_")
    return word.lower()


class PydanticSingleton(ModelMetaclass):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(PydanticSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
