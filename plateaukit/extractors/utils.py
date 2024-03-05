import re
import warnings

from lxml import etree

from plateaukit import constants


def extract_gml_id(tree: etree._Element):
    path = "./[@gml:id]"
    result = tree.find(path, constants.nsmap)

    if result is None:
        warnings.warn(
            "gml:id not found"
            # f"gml:id not found\n{etree.tostring(tree, pretty_print=True).decode()}"
        )
        return None

    id = result.get(f"{{{constants.nsmap['gml']}}}id")

    return id if id is not None else None


def extract_epsg(tree):
    path = "./gml:boundedBy/gml:Envelope"
    result = tree.find(path, constants.nsmap)

    if result is None:
        raise Exception("EPSG not found")

    srs_name = result.get("srsName")

    m = re.match(r"http://www.opengis.net/def/crs/EPSG/0/(\d+)", srs_name)

    if not m:
        raise Exception("Failed to parse EPSG")

    return m.group(1)
