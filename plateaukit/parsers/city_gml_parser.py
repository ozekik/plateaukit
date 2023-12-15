# %%

from dataclasses import dataclass
from typing import Any, BinaryIO

import pyproj
from lxml import etree

from plateaukit import extractors
from plateaukit.parsers.city_object_parser import CityObject, PLATEAUCityObjectParser
from plateaukit.parsers.codelist_parser import CodelistParser
from plateaukit.parsers.constants import nsmap


@dataclass
class CityGML:
    city_objects: list[CityObject]


class CityGMLParser:
    pass


class PLATEAUCityGMLParser(CityGMLParser):
    """A parser for PLATEAU CityGML.

    Attributes:
        target_epsg: Target EPSG code.
        codelist_file_map: A map from codelist path to file object.
    """

    target_epsg: int
    codelist_file_map: dict[str, BinaryIO] | None = None

    def __init__(self, target_epsg: int = 4326, codelist_file_map=None):
        self.target_epsg = target_epsg
        self.codelist_file_map = codelist_file_map

    def parse(self, infile):
        tree = etree.parse(infile)
        root = tree.getroot()

        src_epsg = extractors.utils.extract_epsg(tree)  # 6697

        # TODO: Accept options like always_xy
        transformer = pyproj.Transformer.from_crs(src_epsg, self.target_epsg)

        # Parse codelists
        codelist_map = None

        if self.codelist_file_map:
            codelist_map = dict()

            parser = CodelistParser()

            for path, file_obj in self.codelist_file_map.items():
                codelist = parser.parse(file_obj)
                codelist_map[path] = codelist

        co_parser = PLATEAUCityObjectParser(
            transformer=transformer, codelist_map=codelist_map
        )

        objects = []

        for i, el in enumerate(root.iterfind(f"./core:cityObjectMember/*", nsmap)):
            obj = co_parser.parse(el)

            # print(obj)

            objects.append(obj)

        return CityGML(
            city_objects=objects,
        )

    # def city_objects(self):
    #     pass
