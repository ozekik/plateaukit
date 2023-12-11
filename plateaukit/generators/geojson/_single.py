from geojson import Feature, FeatureCollection, GeometryCollection, Polygon

from plateaukit.logger import logger
from plateaukit.parsers import PLATEAUCityGMLParser
from plateaukit.utils import dict_key_to_camel_case


def geojson_from_gml_single(
    infile,
    types=None,
    target_epsg=4326,  # WGS
    altitude=False,
    lod=[0],
    codelist_file_map=None,
    attributes=["measuredHeight"],
    allow_geometry_collection=False,
):
    # logger.debug("geojson_from_gml_single")

    parser = PLATEAUCityGMLParser(
        target_epsg=target_epsg, codelist_file_map=codelist_file_map
    )
    citygml = parser.parse(infile)

    # logger.debug(f"citygml: {citygml}")

    features = []

    if len(lod) > 1:
        raise NotImplementedError("too many LOD values")

    for i, obj in enumerate(citygml.city_objects):
        logger.debug(f"{obj.id}")

        if types and obj.type not in types:
            continue

        polygons = []

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

        def to_feature(feature_geometry):
            properties = {}
            # properties["id"] = obj.id
            properties |= dict_key_to_camel_case(obj.attributes)
            # if attributes:
            #     properties |= attribute_values

            feat = Feature(
                geometry=feature_geometry,
                properties=properties,
            )

            return feat

        if len(polygons) == 1:
            feat = to_feature(polygons[0])
            features.append(feat)
        else:
            if allow_geometry_collection:
                feat = to_feature(GeometryCollection(polygons))
                features.append(feat)
            else:
                for polygon in polygons:
                    feat = to_feature(polygon)
                    features.append(feat)
                # raise AssertionError("No geometry")

    collection = FeatureCollection(features)

    return collection
