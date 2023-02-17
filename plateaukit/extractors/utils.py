import re
from decimal import Decimal
import warnings

from lxml import etree

from plateaukit.constants import nsmap


def extract_gml_id(tree):
    path = f"./[@{nsmap['gml']}id]"
    result = tree.find(path)
    if result is None:
        warnings.warn(
            "gml:id not found"
            # f"gml:id not found\n{etree.tostring(tree, pretty_print=True).decode()}"
        )
        return None
    id = result.get(f"{nsmap['gml']}id")
    return id if id is not None else None


def extract_name(tree):
    path = f"./{nsmap['gml']}name"
    result = tree.find(path)
    return result.text if result is not None else None


def extract_string_attribute_value(tree, name):
    path = f"./{nsmap['gen']}stringAttribute[@name='{name}']/{nsmap['gen']}value"
    # print(path)
    result = tree.find(path)
    return result.text if result is not None else None


def exract_bldg_attribute(tree, tag):
    path = f"./{nsmap['bldg']}{tag}"
    # print(path)
    result = tree.find(path)
    return result.text if result is not None else None


def extract_address(tree):
    pass


def extract_epsg(tree):
    path = f"./{nsmap['gml']}boundedBy/{nsmap['gml']}Envelope"
    result = tree.find(path)
    if result is None:
        raise Exception("EPSG not found")
    srs_name = result.get("srsName")
    m = re.match(r"http://www.opengis.net/def/crs/EPSG/0/(\d+)", srs_name)
    if not m:
        raise Exception("Failed to parse EPSG")
    return m.group(1)


def extract_lod0_poslists(tree):
    path = "/".join(
        [
            f"./{{*}}lod0RoofEdge",  # TODO: add namespace; should not only RoofEdge
            f"{nsmap['gml']}MultiSurface",
            f"{nsmap['gml']}surfaceMember",
            f"{nsmap['gml']}Polygon",
            f"{nsmap['gml']}exterior",
            f"{nsmap['gml']}LinearRing",
            f"{nsmap['gml']}posList",
        ]
    )
    # print(path)
    results = tree.findall(path)

    if results is None or len(results) == 0:
        return None

    parsed = [list(map(Decimal, result.text.split(" "))) for result in results]

    return parsed


def extract_lod0_poslist(tree):
    parsed = extract_lod0_poslists(tree)

    if len(parsed) > 1:
        raise AssertionError(f"LOD1 has multiple surfaces more than 1:\n{parsed}")

    parsed = parsed[0]

    return parsed


def extract_lod1_poslists(tree):
    path = "/".join(
        [
            f"./{{*}}lod1MultiSurface",  # TODO: add namespace
            f"{nsmap['gml']}MultiSurface",
            f"{nsmap['gml']}surfaceMember",
            f"{nsmap['gml']}Polygon",
            f"{nsmap['gml']}exterior",
            f"{nsmap['gml']}LinearRing",
            f"{nsmap['gml']}posList",
        ]
    )
    # print(path)
    results = tree.findall(path)

    if results is None or len(results) == 0:
        # Fallback
        try:
            parsed = extract_lod2_poslists(tree)
            return parsed
        except:
            # return None
            raise Exception(
                f"Failed to parse:\n{etree.tostring(tree, pretty_print=True).decode()}"
            )

    parsed = [list(map(Decimal, result.text.split(" "))) for result in results]

    return parsed


def extract_lod1_poslist(tree):
    parsed = extract_lod1_poslists(tree)

    if len(parsed) > 1:
        raise AssertionError(f"LOD1 has multiple surfaces more than 1:\n{parsed}")

    parsed = parsed[0]

    return parsed


def extract_lod2_poslists(tree):
    path = "/".join(
        [
            f"./{{*}}lod2MultiSurface",  # TODO: add namespace
            f"{nsmap['gml']}MultiSurface",
            f"{nsmap['gml']}surfaceMember",
            f"{nsmap['gml']}Polygon",
            f"{nsmap['gml']}exterior",
            f"{nsmap['gml']}LinearRing",
            f"{nsmap['gml']}posList",
        ]
    )
    # print(path)
    results = tree.findall(path)

    if results is None or len(results) == 0:
        raise Exception(
            f"Failed to parse:\n{etree.tostring(tree, pretty_print=True).decode()}"
        )

    parsed = [list(map(Decimal, result.text.split(" "))) for result in results]

    return parsed
