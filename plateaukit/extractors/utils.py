import re
import warnings

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
