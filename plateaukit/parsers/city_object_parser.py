from dataclasses import dataclass
from typing import Any

import pyproj

from plateaukit import extractors, utils
from plateaukit.parsers.constants import nsmap

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


class GeometryParser:
    """A parser for CityGML geometries.

    Attributes:
        transformer: A pyproj.Transformer instance.
        maplibre: Whether to use MapLibre scale factor.
    """

    transformer: pyproj.Transformer
    maplibre: bool = False

    def __init__(self, transformer: pyproj.Transformer = None, maplibre: bool = False):
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
        codelist_map: A map from codelist path to corresponding dict.
    """

    transformer: pyproj.Transformer
    codelist_map: dict[str, dict[str, str]] | None = {}

    def __init__(self, transformer: pyproj.Transformer = None, codelist_map={}):
        self.transformer = transformer
        self.codelist_map = codelist_map or {}


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

    def _get_year_of_construction(self, root):
        result = root.find(f"./bldg:yearOfConstruction", nsmap)
        value = result.text if result is not None else None
        value = int(value) if value is not None else None
        return value

    def _get_storeys_above_ground(self, root):
        result = root.find(f"./bldg:storeysAboveGround", nsmap)
        value = result.text if result is not None else None
        value = int(value) if value is not None else None
        return value

    def _get_storeys_below_ground(self, root):
        result = root.find(f"./bldg:storeysBelowGround", nsmap)
        value = result.text if result is not None else None
        value = int(value) if value is not None else None
        return value

    def __get_codespace_attribute(self, root, xpath) -> str | None:
        el = root.find(xpath, nsmap)

        if el is None:
            return None

        # Check if el has codeSpace attribute
        if (code_space_path := el.get("codeSpace")) is not None:
            code_dict = self.codelist_map.get(code_space_path, None)

            if code_dict is None:
                return None

            key = el.text
            value = code_dict.get(key, None)
            return value

        value = el.text if el is not None else None
        return value

    def _get_name(self, root):
        value = self.__get_codespace_attribute(root, "./gml:name")
        return value

    def _get_usage(self, root):
        value = self.__get_codespace_attribute(root, "./bldg:usage")
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

            # Optional attributes
            optional_attributes = {
                "measured_height": self._get_measured_height(el),
                "year_of_construction": self._get_year_of_construction(el),
                "storeys_above_ground": self._get_storeys_above_ground(el),
                "storeys_below_ground": self._get_storeys_below_ground(el),
                "name": self._get_name(el),
                "usage": self._get_usage(el),
            }
            optional_attributes = {
                k: v for k, v in optional_attributes.items() if v is not None
            }
            attributes.update(optional_attributes)

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
        else:
            raise NotImplementedError(f"Unknown object type: {el.tag}")

        return obj
