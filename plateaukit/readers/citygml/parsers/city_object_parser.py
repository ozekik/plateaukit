from dataclasses import dataclass

import pyproj
from lxml import etree

from plateaukit.readers.citygml.constants import default_nsmap
from plateaukit.readers.citygml.extractors import city_object_extractors as extractors
from plateaukit.readers.citygml.ir_models import IRCityObject, IRGeometry
from plateaukit.readers.citygml.parsers.geometry_parser import GeometryParser
from plateaukit.readers.citygml.parsers.xml_models.city_object import CityObjectXML


@dataclass
class Building(IRCityObject):
    address: dict | None = None


class CityObjectParser:
    """A parser for CityGML objects.

    Attributes:
        transformer: A pyproj.Transformer instance.
    """

    transformer: pyproj.Transformer | None
    nsmap: dict[str, str]

    def __init__(
        self,
        *,
        transformer: pyproj.Transformer | None = None,
        nsmap: dict[str, str],
        codelist_map: dict | None = {},
    ):
        self.transformer = transformer
        self.nsmap = nsmap
        self.codelist_map = codelist_map or {}

        self.object_type_tags = {
            "Building": f"{{{default_nsmap['bldg']}}}Building",
            "Road": f"{{{default_nsmap['tran']}}}Road",
            "Bridge": f"{{{default_nsmap['brid']}}}Bridge",
        }

        self.geometry_type_tags = [
            {"type": "lod0RoofEdge", "tag": f"{{{default_nsmap['bldg']}}}lod0RoofEdge"},
            {
                "type": "lod0FootPrint",
                "tag": f"{{{default_nsmap['bldg']}}}lod0FootPrint",
            },
            {"type": "lod1Solid", "tag": f"{{{default_nsmap['bldg']}}}lod1Solid"},
            {"type": "lod2Solid", "tag": f"{{{default_nsmap['bldg']}}}lod2Solid"},
            {
                "type": "lod2MultiSurface",
                "tag": f"{{{default_nsmap['bldg']}}}lod2MultiSurface",
            },
            {
                "type": "lod1MultiSurface",
                "tag": f"{{{default_nsmap['tran']}}}lod1MultiSurface",
            },
            {"type": "lod1Solid", "tag": f"{{{default_nsmap['brid']}}}lod1Solid"},
            {
                "type": "lod2MultiSurface",
                "tag": f"{{{default_nsmap['brid']}}}lod2MultiSurface",
            },
        ]


class PLATEAUCityObjectParser(CityObjectParser):
    """A parser for PLATEAU CityGML objects."""

    def _get_geometry(self, root: etree._Element):
        geoms = []

        parser = GeometryParser(transformer=self.transformer)

        for type_tag in self.geometry_type_tags:
            type = type_tag["type"]
            tag = type_tag["tag"]

            el = root.find(f"./{tag}", self.nsmap)

            if el is None:
                continue

            if type in ["lod0RoofEdge", "lod0FootPrint"]:
                chunked_poslists = parser.extract_chunked_poslists(el)

                geom = IRGeometry(
                    type="MultiSurface",
                    lod="0",
                    boundaries=chunked_poslists,
                    semantics={
                        "surfaces": [
                            {
                                "type": f"+{type}",
                            }
                        ],
                        "values": [0 for _ in range(len(chunked_poslists))],
                    },
                )

                geoms.append(geom)
            elif type in ["lod1MultiSurface"]:
                chunked_poslists = parser.extract_chunked_poslists(el)

                geom = IRGeometry(
                    type="MultiSurface",
                    lod="1",
                    boundaries=chunked_poslists,
                    semantics={
                        "surfaces": [
                            {
                                "type": f"+{type}",
                            }
                        ],
                        "values": [0 for _ in range(len(chunked_poslists))],
                    },
                )

                geoms.append(geom)
            elif type in ["lod1Solid"]:
                # TODO: Fix this
                chunked_poslists = parser.extract_chunked_poslists(el)
                solid_boundaries = [chunked_poslists]

                geom = IRGeometry(
                    type="Solid",
                    lod="1",
                    boundaries=solid_boundaries,
                    semantics={
                        "surfaces": [
                            {
                                "type": f"+{type}",
                            }
                        ],
                        "values": [0 for _ in range(len(solid_boundaries))],
                    },
                )

                geoms.append(geom)
            elif type in ["lod2MultiSurface"]:
                chunked_poslists = parser.extract_chunked_poslists(el)

                geom = IRGeometry(
                    type="MultiSurface",
                    lod="2",
                    boundaries=chunked_poslists,
                    semantics={
                        "surfaces": [
                            {
                                "type": f"+{type}",
                            }
                        ],
                        "values": [0 for _ in range(len(chunked_poslists))],
                    },
                )

                geoms.append(geom)

        # NOTE: Process boundedBy for Building and Bridge

        if root.tag in [
            self.object_type_tags["Building"],
            self.object_type_tags["Bridge"],
        ]:
            # Look through boundedBy
            # TODO: Fix these conditions
            if root.tag == self.object_type_tags["Building"] and "bldg" in self.nsmap:
                bound_els = list(root.iterfind("./bldg:boundedBy", self.nsmap))
            elif root.tag == self.object_type_tags["Bridge"] and "brid" in self.nsmap:
                bound_els = list(root.iterfind("./brid:boundedBy", self.nsmap))
            else:
                # TODO: Fix this
                raise NotImplementedError()
                # print("self.nsmap", self.nsmap)
                # exit()
                # bound_els = []

            for bound_el in bound_els:
                # TODO: Check semantics
                for type_tag in self.geometry_type_tags:
                    type = type_tag["type"]
                    tag = type_tag["tag"]

                    el = bound_el.find(f".//{tag}", self.nsmap)

                    if el is None:
                        continue

                    if type in ["lod2MultiSurface"]:
                        chunked_poslists = parser.extract_chunked_poslists(el)

                        geom = IRGeometry(
                            type="MultiSurface",
                            lod="2",
                            boundaries=chunked_poslists,
                            semantics={
                                "surfaces": [
                                    {
                                        "type": f"+{type}",
                                    }
                                ],
                                "values": [0 for _ in range(len(chunked_poslists))],
                            },
                        )

                        geoms.append(geom)

                    else:
                        pass
                        # raise NotImplementedError()
        # elif root.tag == self.object_type_tags["Road"]:
        #     pass
        # else:
        #     raise NotImplementedError(f"Failed to parse geometry for {root.tag}")

        return geoms

    def _parse_attributes(self, el: CityObjectXML) -> dict:
        # TODO: parse `uro:` attributes

        attributes = dict()

        if el.tree.tag == self.object_type_tags["Building"]:
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

            # river_flooding_risks = extractors.get_river_flooding_risks(el)
            # river_flooding_risk_attributes = {}
            # for name, dic in river_flooding_risks.items():
            #     for item_key, value in dic.items():
            #         key = f"river_flooding_risk.{name}.{item_key}"
            #         river_flooding_risk_attributes[key] = value
            # optional_attributes.update(river_flooding_risk_attributes)

            # TODO: Delete column if all values are empty (elsewhere)

            river_flooding_risks = extractors.get_river_flooding_risks(el)
            optional_attributes.update({"river_flooding_risk": river_flooding_risks})

            optional_attributes = {
                k: v for k, v in optional_attributes.items() if v is not None
            }
            attributes.update(optional_attributes)
        elif el.tree.tag == self.object_type_tags["Bridge"]:
            attributes["_gml_id"] = el.get_gml_id()

        return attributes

    def parse(self, element: etree._Element) -> IRCityObject:
        el = CityObjectXML(element, nsmap=self.nsmap, codelist_map=self.codelist_map)

        citygml_id = el.get_gml_id()
        address = None  # self._get_address(el)

        attributes = self._parse_attributes(el)

        if el.tree.tag == self.object_type_tags["Building"]:
            attributes["building_id"] = extractors.get_building_id(el)

            geometry = self._get_geometry(el.tree)

            obj = Building(
                type="Building",
                id=citygml_id,
                attributes=attributes,
                geometry=geometry,
                address=address,
            )
        elif el.tree.tag == self.object_type_tags["Road"]:
            geometry = self._get_geometry(el.tree)

            obj = IRCityObject(
                type="Road",
                id=citygml_id,
                attributes=attributes,
                geometry=geometry,
            )
        elif el.tree.tag == self.object_type_tags["Bridge"]:
            geometry = self._get_geometry(el.tree)

            obj = IRCityObject(
                type="Bridge",
                id=citygml_id,
                attributes=attributes,
                geometry=geometry,
            )
        else:
            raise NotImplementedError(f"Unknown object type: {el.tree.tag}")
            # warnings.warn(f"Unknown object type: {el.tree.tag}")

        return obj
