import re
from typing import BinaryIO

import pyproj
from lxml import etree

from plateaukit.formats.citygml import CityGML
from plateaukit.formats.citygml.constants import nsmap
from plateaukit.formats.citygml.parsers.city_object_parser import (
    PLATEAUCityObjectParser,
)
from plateaukit.formats.citygml.parsers.codelist_parser import CodelistParser


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

    def _get_epsg_code(self, tree: etree._ElementTree) -> str | None:
        """Extract EPSG code from CityGML tree."""

        path = "./gml:boundedBy/gml:Envelope"
        result = tree.find(path, nsmap)
        result = result if result is not None else {}
        srs_name = result.get("srsName")

        if srs_name is None:
            raise Exception("EPSG code not found")

        m = re.match(r"http://www.opengis.net/def/crs/EPSG/0/(\d+)", srs_name)

        if not m:
            raise Exception("Failed to parse EPSG code")

        return m.group(1)

    def parse(self, infile, selection: list[str] | None = None):
        tree = etree.parse(infile)
        root = tree.getroot()

        src_epsg = self._get_epsg_code(tree)  # 6697

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

        for i, el in enumerate(root.iterfind("./core:cityObjectMember/*", nsmap)):
            obj = co_parser.parse(el)

            # TODO: Improve performance
            building_id = (
                obj.attributes.get("building_id", None) if obj.attributes else None
            )
            if selection and (
                obj.id not in selection and (building_id not in selection)
            ):
                continue

            objects.append(obj)

        return CityGML(city_objects=objects)
