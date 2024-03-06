from plateaukit.parsers.constants import nsmap


def _get_string_attribute(root, name) -> str | None:
    path = f"./gen:stringAttribute[@name='{name}']/gen:value"
    result = root.find(path, nsmap)
    return result.text if result is not None else None


def _get_building_id(root) -> str | None:
    try:
        path = "./uro:buildingIDAttribute/uro:BuildingIDAttribute/uro:buildingID"
        result = root.find(path, nsmap)
        value = result.text if result is not None else None
        assert value is not None
        return value
    except:
        pass

    try:
        value = _get_string_attribute(root, name="建物ID")
        assert value is not None
        return value
    except:
        pass

    return None


def _get_measured_height(root) -> float | None:
    result = root.find("./bldg:measuredHeight", nsmap)
    value = result.text if result is not None else None
    value = float(value) if value is not None else None
    return value


def _get_year_of_construction(root) -> int | None:
    result = root.find("./bldg:yearOfConstruction", nsmap)
    value = result.text if result is not None else None
    value = int(value) if value is not None else None
    return value


def _get_storeys_above_ground(root) -> int | None:
    result = root.find("./bldg:storeysAboveGround", nsmap)
    value = result.text if result is not None else None
    value = int(value) if value is not None else None
    return value


def _get_storeys_below_ground(root) -> int | None:
    result = root.find("./bldg:storeysBelowGround", nsmap)
    value = result.text if result is not None else None
    value = int(value) if value is not None else None
    return value


def _get_address(root) -> dict | None:
    el = root.find("./bldg:address", nsmap)
    locality_name = el.find(".//xAL:LocalityName", nsmap).text

    addr = {
        "locality_name": locality_name,
    }

    return addr
