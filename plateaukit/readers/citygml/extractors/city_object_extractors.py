from plateaukit.readers.citygml.parsers.xml_models.city_object import CityObjectXML


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


def get_district_plan(xml: CityObjectXML) -> str | None:
    value = _get_string_attribute(xml, name="地区計画")
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


def get_river_flooding_risks(xml: CityObjectXML):
    results = xml.iterfind(
        "./uro:buildingDisasterRiskAttribute/uro:BuildingRiverFloodingRiskAttribute",
        xml.nsmap,
    )
    value = {}
    for result in results:
        description = xml._get_codespace_attribute("./uro:description", parent=result)

        # rank = xml._get_codespace_attribute("./uro:rank", parent=result)
        # rank_org = xml._get_codespace_attribute("./uro:rankOrg", parent=result)

        depth = result.find("./uro:depth", xml.nsmap)
        depth = float(depth.text) if depth is not None else None

        duration = result.find("./uro:duration", xml.nsmap)
        duration = float(duration.text) if duration is not None else None

        admin_type = xml._get_codespace_attribute("./uro:adminType", parent=result)

        scale = xml._get_codespace_attribute("./uro:scale", parent=result)

        value[description] = {
            # "rank": rank,
            # "rankOrg": rank_org,
            "depth": depth,
            "duration": duration,
            "adminType": admin_type,
            "scale": scale,
        }

    return value


def get_river_flooding_depth(xml: CityObjectXML) -> float | None:
    result = xml.find(
        "./uro:buildingDisasterRiskAttribute/uro:BuildingRiverFloodingRiskAttribute/uro:depth",
        xml.nsmap,
    )
    value = result.text if result is not None else None
    value = float(value) if value is not None else None
    return value


def get_river_flooding_duration(xml: CityObjectXML) -> float | None:
    result = xml.find(
        "./uro:buildingDisasterRiskAttribute/uro:BuildingRiverFloodingRiskAttribute/uro:duration",
        xml.nsmap,
    )
    value = result.text if result is not None else None
    value = float(value) if value is not None else None
    return value


def get_districts_and_zones_type(xml: CityObjectXML) -> str | None:
    el = xml.find(
        "./uro:buildingDetailAttribute",
        xml.nsmap,
    )

    if el is None:
        return None

    # TODO:
    # ".//uro:urbanPlanType", # "都市計画区域" など
    # ".//uro:areaClassificationType",  # "市街化区域" など

    # 都市計画法第8条第3項第1号に定める地域地区（及び用途地域）の区分
    result = xml._get_codespace_attribute(
        "./uro:BuildingDetailAttribute/uro:districtsAndZonesType", parent=el
    )

    return result


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
