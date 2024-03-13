from dataclasses import dataclass

import pyproj
from lxml import etree

from plateaukit import utils
from plateaukit.formats.citygml import CityObject
from plateaukit.formats.citygml.constants import nsmap
from plateaukit.formats.citygml.extractors import city_object_extractors as extractors
from plateaukit.formats.citygml.parsers.xml_models.city_object import CityObjectXML

MAPLIBRE_SCALE_FACTOR = 10000000
MERCATOR_HALF_WORLD_LENGTH = 20037508.342789243906736373901367187500

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


@dataclass
class Building(CityObject):
    address: dict | None = None


class GeometryParser:
    """A parser for CityGML geometries.

    Attributes:
        transformer: A pyproj.Transformer instance.
        maplibre: Whether to use MapLibre scale factor.
    """

    transformer: pyproj.Transformer | None
    maplibre: bool = False

    def __init__(
        self, transformer: pyproj.Transformer | None = None, maplibre: bool = False
    ):
        self.transformer = transformer
        self.maplibre = maplibre

    def _transform(self, vertices, scale=(1, 1, 1), translate=(0, 0, 0)):
        # TODO: numpy

        transformed = []

        for vertex in vertices:
            x, y, z = vertex
            nx = (x * scale[0]) + translate[0]
            ny = (y * scale[1]) + translate[1]
            nz = (z * scale[2]) + translate[2]
            transformed.append((nx, ny, nz))

        return transformed

    def _adjust_mercator_to_maplibre(self, vertices):
        transformed = self._transform(
            vertices,
            scale=[-(0.5 * MAPLIBRE_SCALE_FACTOR) / MERCATOR_HALF_WORLD_LENGTH] * 2
            + [0.5 * MAPLIBRE_SCALE_FACTOR / MERCATOR_HALF_WORLD_LENGTH],
            translate=(
                0.5 * MAPLIBRE_SCALE_FACTOR,
                0.5 * MAPLIBRE_SCALE_FACTOR,
                0,
            ),
        )

        return transformed

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

        parsed = []

        for result in results:
            poslist = list(map(float, result.text.split(" ")))

            chunked = list(utils.chunker(poslist, 3))

            if self.maplibre and self.transformer:
                chunked = list(self.transformer.itransform(chunked))
                chunked = self._adjust_mercator_to_maplibre(chunked)
            elif self.transformer:
                chunked = list(self.transformer.itransform(chunked))

            surface = [chunked]
            parsed.append(surface)

        return parsed


class CityObjectParser:
    """A parser for CityGML objects.

    Attributes:
        transformer: A pyproj.Transformer instance.
    """

    transformer: pyproj.Transformer | None

    def __init__(self, transformer: pyproj.Transformer | None = None, codelist_map={}):
        self.transformer = transformer
        self.codelist_map = codelist_map or {}


class PLATEAUCityObjectParser(CityObjectParser):
    def _get_geometry(self, root: etree._Element):
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

    def _parse_attributes(self, el: CityObjectXML) -> dict:
        # TODO: parse `uro:` attributes

        attributes = dict()

        if el.tree.tag == object_type_tags["Building"]:
            attributes["building_id"] = extractors.get_building_id(el)

            # Optional attributes
            # TODO: Change extractors to transformers
            optional_attributes = {
                "measured_height": extractors.get_measured_height(el),
                "year_of_construction": extractors.get_year_of_construction(el),
                "storeys_above_ground": extractors.get_storeys_above_ground(el),
                "storeys_below_ground": extractors.get_storeys_below_ground(el),
                "name": extractors.get_name(el),
                "usage": extractors.get_usage(el),
            }
            optional_attributes = {
                k: v for k, v in optional_attributes.items() if v is not None
            }
            attributes.update(optional_attributes)

        return attributes

    def parse(self, element: etree._Element) -> CityObject:
        el = CityObjectXML(element, codelist_map=self.codelist_map)

        citygml_id = el.get_gml_id()
        address = None  # self._get_address(el)

        attributes = self._parse_attributes(el)

        if el.tree.tag == object_type_tags["Building"]:
            attributes["building_id"] = extractors.get_building_id(el)

            geometry = self._get_geometry(el.tree)

            obj = Building(
                type="Building",
                id=citygml_id,
                attributes=attributes,
                geometry=geometry,
                address=address,
            )
        elif el.tree.tag == object_type_tags["Road"]:
            geometry = self._get_geometry(el.tree)

            obj = CityObject(
                type="Road",
                id=citygml_id,
                attributes=attributes,
                geometry=geometry,
            )
        elif el.tree.tag == object_type_tags["Bridge"]:
            geometry = self._get_geometry(el.tree)

            obj = CityObject(
                type="Bridge",
                id=citygml_id,
                attributes=attributes,
                geometry=geometry,
            )
        else:
            raise NotImplementedError(f"Unknown object type: {el.tree.tag}")

        return obj
