from dataclasses import dataclass
from typing import Any


@dataclass
class CityObject:
    """A CityGML CityObject."""

    type: str
    id: str | None = None
    attributes: dict[str, Any] | None = None
    geometry: list[Any] | None = None
    # children: list[Self] | None = None
    # parent: Self | None = None


# TODO: boundedBy
