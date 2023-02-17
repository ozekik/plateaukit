from itertools import islice
from decimal import Decimal


def chunker(it, size):
    """Turn an iterable into a tuple of chunks in a specified size."""
    iterator = iter(it)
    while chunk := tuple(islice(iterator, size)):
        yield chunk


def parse_posList(text):
    """Parse a posList string into a list of 3-chunks."""
    points = text.split(" ")
    points = list(map(lambda x: Decimal(x), points))
    # TODO: fix
    points = list(map(lambda x: float(x), points))
    chunks = list(chunker(points, 3))
    return chunks
