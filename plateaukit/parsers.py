# %%

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Self

import pyproj
from lxml import etree

from plateaukit import extractors, utils

nsmap = {
    "gen": "http://www.opengis.net/citygml/generics/2.0",
    "gml": "http://www.opengis.net/gml",
    "core": "http://www.opengis.net/citygml/2.0",
    "bldg": "http://www.opengis.net/citygml/building/2.0",
    "tran": "http://www.opengis.net/citygml/transportation/2.0",
    "brid": "http://www.opengis.net/citygml/bridge/2.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "xAL": "urn:oasis:names:tc:ciq:xsdschema:xAL:2.0",
    "uro": "https://www.geospatial.jp/iur/uro/2.0",
}

object_type_tags = {
    "Building": f"{{{nsmap['bldg']}}}Building",
    "Road": f"{{{nsmap['tran']}}}Road",
    "Bridge": f"{{{nsmap['brid']}}}Bridge",
}

geometry_type_tags = [
    {"type": "lod0RoofEdge", "tag": f"{{{nsmap['bldg']}}}lod0RoofEdge"},
    {"type": "lod0FootPrint", "tag": f"{{{nsmap['bldg']}}}lod0FootPrint"},
    {"type": "lod1Solid", "tag": f"{{{nsmap['bldg']}}}lod1Solid"},
    {"type": "lod2Solid", "tag": f"{{{nsmap['bldg']}}}lod2Solid"},
    {"type": "lod2MultiSurface", "tag": f"{{{nsmap['bldg']}}}lod2MultiSurface"},
    {"type": "lod1MultiSurface", "tag": f"{{{nsmap['tran']}}}lod1MultiSurface"},
    {"type": "lod2MultiSurface", "tag": f"{{{nsmap['brid']}}}lod2MultiSurface"},
]

# TODO: boundedBy


@dataclass
class CityObject:
    type: str
    id: str | None = None
    attributes: dict | None = None
    geometry: list[Any] | None = None
    # children: list[Self] | None = None
    # parent: Self | None = None


@dataclass
class Building(CityObject):
    address: dict | None = None


@dataclass
class CityGML:
    city_objects: list[CityObject]


class GeometryParser:
    def __init__(self, transformer: pyproj.Transformer = None):
        self.transformer = transformer

    def extract_chunked_poslists(self, root):
        path = "/".join(
            [
                ".//gml:surfaceMember",  # TODO: Check this
                "gml:Polygon",
                "gml:exterior",
                "gml:LinearRing",
                "gml:posList",
            ]
        )
        # print(path)
        results = root.findall(path, nsmap)

        # parsed = [list(map(Decimal, result.text.split(" "))) for result in results]
        parsed = []
        for result in results:
            poslist = list(map(float, result.text.split(" ")))
            chunked = list(utils.chunker(poslist, 3))
            if self.transformer:
                chunked = list(self.transformer.itransform(chunked))
            surface = [chunked]
            parsed.append(surface)

        return parsed


class CityObjectParser:
    transformer: pyproj.Transformer

    def __init__(self, transformer: pyproj.Transformer = None):
        self.transformer = transformer


class PLATEAUCityObjectParser(CityObjectParser):
    # TODO: uro: attributes

    def _get_string_attribute(self, root, name):
        path = f"./gen:stringAttribute[@name='{name}']/gen:value"
        result = root.find(path, nsmap)
        return result.text if result is not None else None

    def _get_building_id(self, root):
        try:
            path = "./uro:buildingIDAttribute/uro:BuildingIDAttribute/uro:buildingID"
            result = root.find(path, nsmap)
            value = result.text if result is not None else None
            assert value is not None
            return value
        except:
            pass

        try:
            value = self._get_string_attribute(root, name="建物ID")
            assert value is not None
            return value
        except:
            pass

        return None

    def _get_measured_height(self, root):
        result = root.find(f"./bldg:measuredHeight", nsmap)
        value = result.text if result is not None else None
        value = float(value) if value is not None else None
        return value

    def _get_address(self, root):
        el = root.find(f"./bldg:address", nsmap)
        locality_name = el.find(f".//xAL:LocalityName", nsmap).text

        addr = {
            "locality_name": locality_name,
        }

        # print(addr)

        return addr

    def _get_geometry(self, root):
        geoms = []

        parser = GeometryParser(transformer=self.transformer)

        for type_tag in geometry_type_tags:
            type = type_tag["type"]
            tag = type_tag["tag"]

            el = root.find(f"./{tag}", nsmap)

            if el is None:
                continue

            if type in ["lod0RoofEdge", "lod0FootPrint"]:
                chunked_poslists = parser.extract_chunked_poslists(el)

                geom = {
                    "type": "MultiSurface",
                    "lod": 0,
                    "boundaries": chunked_poslists,
                    "semantics": {
                        "surfaces": [
                            {
                                "type": f"+{type}",
                            }
                        ],
                        "values": [0 for _ in range(len(chunked_poslists))],
                    },
                }

                geoms.append(geom)
            elif type in ["lod1MultiSurface"]:
                chunked_poslists = parser.extract_chunked_poslists(el)

                geom = {
                    "type": "MultiSurface",
                    "lod": 1,
                    "boundaries": chunked_poslists,
                    "semantics": {
                        "surfaces": [
                            {
                                "type": f"+{type}",
                            }
                        ],
                        "values": [0 for _ in range(len(chunked_poslists))],
                    },
                }

                geoms.append(geom)
            elif type in ["lod1Solid"]:
                # TODO: Fix this
                chunked_poslists = parser.extract_chunked_poslists(el)
                solid_boundaries = [chunked_poslists]

                geom = {
                    "type": "Solid",
                    "lod": 1,
                    "boundaries": solid_boundaries,
                    "semantics": {
                        "surfaces": [
                            {
                                "type": f"+{type}",
                            }
                        ],
                        "values": [0 for _ in range(len(solid_boundaries))],
                    },
                }

                geoms.append(geom)
            elif type in ["lod2MultiSurface"]:
                chunked_poslists = parser.extract_chunked_poslists(el)

                geom = {
                    "type": "MultiSurface",
                    "lod": 2,
                    "boundaries": chunked_poslists,
                    "semantics": {
                        "surfaces": [
                            {
                                "type": f"+{type}",
                            }
                        ],
                        "values": [0 for _ in range(len(chunked_poslists))],
                    },
                }

                geoms.append(geom)

        # Look through boundedBy
        bound_els = list(root.iterfind("./bldg:boundedBy", nsmap))
        for bound_el in bound_els:
            # TODO: Check semantics
            for type_tag in geometry_type_tags:
                type = type_tag["type"]
                tag = type_tag["tag"]

                el = bound_el.find(f".//{tag}", nsmap)

                if el is None:
                    continue

                if type in ["lod2MultiSurface"]:
                    chunked_poslists = parser.extract_chunked_poslists(el)

                    geom = {
                        "type": "MultiSurface",
                        "lod": 2,
                        "boundaries": chunked_poslists,
                        "semantics": {
                            "surfaces": [
                                {
                                    "type": f"+{type}",
                                }
                            ],
                            "values": [0 for _ in range(len(chunked_poslists))],
                        },
                    }

                    geoms.append(geom)

                else:
                    pass
                    # raise NotImplementedError()

        return geoms

    def parse(self, el):
        citygml_id = extractors.utils.extract_gml_id(el)
        address = None  # self._get_address(el)

        attributes = dict()

        if el.tag == object_type_tags["Building"]:
            attributes["building_id"] = self._get_building_id(el)
            attributes["measured_height"] = self._get_measured_height(el)

            geometry = self._get_geometry(el)

            obj = Building(
                type="Building",
                id=citygml_id,
                attributes=attributes,
                geometry=geometry,
                address=address,
            )
        elif el.tag == object_type_tags["Road"]:
            geometry = self._get_geometry(el)

            obj = CityObject(
                type="Road",
                id=citygml_id,
                attributes=attributes,
                geometry=geometry,
            )
        elif el.tag == object_type_tags["Bridge"]:
            geometry = self._get_geometry(el)

            obj = CityObject(
                type="Bridge",
                id=citygml_id,
                attributes=attributes,
                geometry=geometry,
            )

        return obj


class CityGMLParser:
    pass


class PLATEAUCityGMLParser(CityGMLParser):
    """A parser for PLATEAU CityGML."""

    def __init__(self, target_epsg=4326):
        self.target_epsg = target_epsg

    def parse(self, infile):
        tree = etree.parse(infile)
        root = tree.getroot()

        src_epsg = extractors.utils.extract_epsg(tree)  # 6697

        transformer = pyproj.Transformer.from_crs(src_epsg, self.target_epsg)

        objects = []

        co_parser = PLATEAUCityObjectParser(transformer=transformer)

        for i, el in enumerate(root.iterfind(f"./core:cityObjectMember/*", nsmap)):
            obj = co_parser.parse(el)

            # print(obj)

            objects.append(obj)

        return CityGML(
            city_objects=objects,
        )

    # def city_objects(self):
    #     pass
