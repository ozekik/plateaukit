from typing import Any, BinaryIO

from geojson import Feature, FeatureCollection, GeometryCollection, Polygon

from plateaukit.formats.citygml import PLATEAUCityGMLParser
from plateaukit.logger import logger
from plateaukit.utils import dict_key_to_camel_case


def _to_feature(feature_geometry, *, properties: dict[str, Any]):
    _properties = {}

    # _properties["id"] = ...?

    _properties |= dict_key_to_camel_case(properties)

    feat = Feature(
        geometry=feature_geometry,
        properties=_properties,
    )

    return feat


def features_from_gml_single(
    infile: BinaryIO,
    types: list[str] | None = None,
    target_epsg: int = 4326,  # WGS
    altitude: bool = False,
    lod: list[int] = [0],
    codelist_file_map: dict[str, BinaryIO] | None = None,
    attributes: list[str] = ["measuredHeight"],
    allow_geometry_collection: bool = False,
    include_type: bool = False,
):
    """Generate GeoJSON from a single CityGML file."""

    # logger.debug("geojson_from_gml_single")

    parser = PLATEAUCityGMLParser(
        target_epsg=target_epsg, codelist_file_map=codelist_file_map
    )
    co_iter = parser.iterparse(infile)

    # logger.debug(f"citygml: {citygml}")

    if len(lod) > 1:
        raise NotImplementedError("too many LOD values")

    for i, obj in enumerate(co_iter):
        # logger.debug(f"{obj.id}")  # NOTE: Affect performance

        if types and obj.type not in types:
            continue

        geom = None

        if 0 in lod:
            geom = next(filter(lambda x: x["lod"] == 0, obj.geometry), None)
        if 1 in lod:
            geom = next(filter(lambda x: x["lod"] == 1, obj.geometry), None)
            # raise NotImplementedError("LOD 1")
        if 2 in lod:
            geom = next(filter(lambda x: x["lod"] == 2, obj.geometry), None)

        if geom is None:
            continue

        # WIP: exterior only; TODO: Fix this
        base_polygons = [surface[0] for surface in geom["boundaries"]]

        if altitude:
            base_polygons = [
                list(map(lambda x: [x[1], x[0], x[2]], base_polygon))
                for base_polygon in base_polygons
            ]
        else:
            base_polygons = [
                list(map(lambda x: [x[1], x[0]], base_polygon))
                for base_polygon in base_polygons
            ]

        polygons = [Polygon([base_polygon]) for base_polygon in base_polygons]

        properties = dict(obj.attributes) if obj.attributes else {}

        if include_type:
            properties["type"] = obj.type

        if len(polygons) == 1:
            feat = _to_feature(polygons[0], properties=properties)
            yield feat
        else:
            if allow_geometry_collection:
                feat = _to_feature(GeometryCollection(polygons), properties=properties)
                yield feat
            else:
                for polygon in polygons:
                    feat = _to_feature(polygon, properties=properties)
                    yield feat
                # raise AssertionError("No geometry")


def geojson_from_gml_single(
    infile: BinaryIO,
    types: list[str] | None = None,
    target_epsg: int = 4326,  # WGS
    altitude: bool = False,
    lod: list[int] = [0],
    codelist_file_map: dict[str, BinaryIO] | None = None,
    attributes: list[str] = ["measuredHeight"],
    allow_geometry_collection: bool = False,
    include_type: bool = False,
):
    """Generate GeoJSON from a single CityGML file."""

    features = list(
        features_from_gml_single(
            infile,
            types=types,
            target_epsg=target_epsg,
            altitude=altitude,
            lod=lod,
            codelist_file_map=codelist_file_map,
            attributes=attributes,
            allow_geometry_collection=allow_geometry_collection,
            include_type=include_type,
        )
    )
    collection = FeatureCollection(features)

    return collection
