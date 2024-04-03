from plateaukit.formats.citygml.parsers.xml_models.city_object import CityObjectXML


def _get_string_attribute(xml: CityObjectXML, name) -> str | None:
    path = f"./gen:stringAttribute[@name='{name}']/gen:value"
    result = xml.find(path, xml.nsmap)
    return result.text if result is not None else None


def get_name(xml: CityObjectXML) -> str | None:
    value = xml._get_codespace_attribute("./gml:name")
    return value


def get_usage(xml: CityObjectXML) -> str | None:
    value = xml._get_codespace_attribute("./bldg:usage")
    return value


def get_building_id(xml: CityObjectXML) -> str | None:
    try:
        path = "./uro:buildingIDAttribute/uro:BuildingIDAttribute/uro:buildingID"
        result = xml.find(path, xml.nsmap)
        value = result.text if result is not None else None
        assert value is not None
        return value
    except AssertionError:
        pass

    try:
        value = _get_string_attribute(xml, name="建物ID")
        assert value is not None
        return value
    except AssertionError:
        pass

    return None


def get_measured_height(xml: CityObjectXML) -> float | None:
    result = xml.find("./bldg:measuredHeight", xml.nsmap)
    value = result.text if result is not None else None
    value = float(value) if value is not None else None
    return value


def get_year_of_construction(xml: CityObjectXML) -> int | None:
    result = xml.find("./bldg:yearOfConstruction", xml.nsmap)
    value = result.text if result is not None else None
    value = int(value) if value is not None else None
    return value


def get_storeys_above_ground(xml: CityObjectXML) -> int | None:
    result = xml.find("./bldg:storeysAboveGround", xml.nsmap)
    value = result.text if result is not None else None
    value = int(value) if value is not None else None
    return value


def get_storeys_below_ground(xml: CityObjectXML) -> int | None:
    result = xml.find("./bldg:storeysBelowGround", xml.nsmap)
    value = result.text if result is not None else None
    value = int(value) if value is not None else None
    return value


def get_address(xml: CityObjectXML) -> dict | None:
    el = xml.find("./bldg:address", xml.nsmap)

    if el is None:
        return None

    result = el.find(".//xAL:LocalityName", xml.nsmap)

    if result is None:
        return None

    locality_name = result.text

    addr = {
        "locality_name": locality_name,
    }

    return addr
