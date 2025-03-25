import re
import warnings
from io import IOBase
from itertools import chain
from typing import BinaryIO

import pyproj
from lxml import etree

from plateaukit.readers.citygml.constants import default_nsmap
from plateaukit.readers.citygml.ir_models import IRDocument
from plateaukit.readers.citygml.parsers.city_object_parser import (
    PLATEAUCityObjectParser,
)
from plateaukit.readers.citygml.parsers.codelist_parser import CodelistParser


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

    def _get_epsg_code(self, infile: IOBase) -> str | None:
        """Extract EPSG code from CityGML tree."""
        tag = f"{{{default_nsmap['gml']}}}boundedBy"
        path = "gml:Envelope"

        srs_name = None
        for _ev, el in etree.iterparse(infile, events=("end",), tag=tag):
            result = el.find(path, default_nsmap)
            found = result is not None
            if result is not None:
                srs_name = result.get("srsName")
                break
            el.clear()

        if srs_name is None:
            raise Exception("EPSG code not found")

        m = re.match(r"http://www.opengis.net/def/crs/EPSG/0/(\d+)", srs_name)

        if not m:
            raise Exception("Failed to parse EPSG code")

        infile.seek(0)

        return m.group(1)

    def _get_nsmap(self, infile: IOBase) -> dict[str, str]:
        """Extract namespace map from CityGML document."""

        itertree = etree.iterparse(infile)
        _, root = next(itertree)
        nsmap = root.nsmap

        infile.seek(0)

        return nsmap  # TODO: Fix typing

    def iterparse(self, infile, selection: list[str] | None = None):
        src_epsg = self._get_epsg_code(infile)  # 6697

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

        nsmap = self._get_nsmap(infile)

        co_parser = PLATEAUCityObjectParser(
            transformer=transformer, nsmap=nsmap, codelist_map=codelist_map
        )

        tag = f"{{{nsmap['core']}}}cityObjectMember"

        itertree = etree.iterparse(infile, events=("end",), tag=tag)
        _, root = next(itertree)

        dirty = False

        for _ev, el in chain([(_, root)], itertree):
            it = el.iterchildren()
            co_element = next(it)
            try:
                obj = co_parser.parse(co_element)
            except Exception as e:
                warnings.warn(str(e))
                dirty = True
                continue

            # TODO: Improve performance
            # building_id = (
            #     obj.attributes.get("building_id", None) if obj.attributes else None
            # )
            if selection and (obj.id not in selection and (obj.id not in selection)):
                continue

            yield obj

            # NOTE: `if not dirty` is somehow required to avoid stucking in the loop
            if not dirty:
                el.clear()
                root.clear()

        infile.seek(0)

    def parse(self, infile, selection: list[str] | None = None):
        src_epsg = self._get_epsg_code(infile)  # 6697

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

        nsmap = self._get_nsmap(infile)

        co_parser = PLATEAUCityObjectParser(
            transformer=transformer, nsmap=nsmap, codelist_map=codelist_map
        )

        objects = []

        tag = f"{{{nsmap['core']}}}cityObjectMember"

        itertree = etree.iterparse(infile, events=("end",), tag=tag)
        _, root = next(itertree)

        for _ev, el in itertree:
            it = el.iterchildren()
            co_element = next(it)

            try:
                obj = co_parser.parse(co_element)
            except Exception as e:
                warnings.warn(str(e))
                continue

            # TODO: Improve performance
            building_id = (
                obj.attributes.get("building_id", None) if obj.attributes else None
            )
            if selection and (
                obj.id not in selection and (building_id not in selection)
            ):
                continue

            # TODO: Memory optimization
            objects.append(obj)

            el.clear()
            root.clear()

        infile.seek(0)

        return IRDocument(metadata=None, city_objects=objects)
