from dataclasses import dataclass
from typing import Any


@dataclass
class IRGeometry:
    """A CityGML Geometry."""

    type: str
    lod: str
    boundaries: list[Any]
    semantics: dict[str, Any] | None = None


@dataclass
class IRCityObject:
    """A CityGML CityObject."""

    type: str
    id: str | None  # TODO: Make id required
    geometry: list[IRGeometry]
    attributes: dict[str, Any] | None = None
    # children: list[Self] | None = None
    # parent: Self | None = None


@dataclass
class IRMetadata:
    epsg: int


@dataclass
class IRDocument:
    """A CityGML document (Metadata and a collection of CityObjects)"""

    metadata: Any
    city_objects: list[IRCityObject]
