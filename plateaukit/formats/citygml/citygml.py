from dataclasses import dataclass

from plateaukit.formats.citygml.city_object import CityObject


@dataclass
class CityGML:
    city_objects: list[CityObject]
