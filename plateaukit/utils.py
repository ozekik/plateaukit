from decimal import Decimal
from itertools import islice
from typing import Any, Iterable


def chunker(it: Iterable, size: int):
    """Turn an iterable into a tuple of chunks in a specified size."""

    iterator = iter(it)
    while chunk := tuple(islice(iterator, size)):
        yield chunk


def parse_posList(text: str):
    """Parse a posList string into a list of 3-chunks."""

    points = text.split(" ")
    points = list(map(lambda x: Decimal(x), points))
    # TODO: fix
    points = list(map(lambda x: float(x), points))
    chunks = list(chunker(points, 3))
    return chunks


def dict_key_to_camel_case(d: dict[str, Any]):
    """Convert dictionary keys to camelCase."""

    def to_camel_case(s):
        t = "".join([w.capitalize() for w in s.split("_")])
        return t[0].lower() + t[1:]

    return {to_camel_case(k): v for k, v in d.items()}
