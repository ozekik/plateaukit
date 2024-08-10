from dataclasses import dataclass

from plateaukit.readers.citygml.city_object import CityObject


@dataclass
class CityGML:
    """A CityGML document/dataset."""

    city_objects: list[CityObject]
