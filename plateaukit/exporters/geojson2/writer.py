from typing import Any

from geojson import Feature, FeatureCollection, GeometryCollection, Polygon

from plateaukit.readers.citygml.ir_models import IRDocument
from plateaukit.utils import dict_key_to_camel_case

# @dataclass
# class IndexedGeometry:
#     type: str
#     boundaries: list[Any]
#     lod: str | None = None


class FeatureGenerator:
    def __init__(
        self,
        altitude: bool = False,
        include_object_type: bool = True,
        allow_geometry_collection: bool = True,
    ):
        self.altitude = altitude
        self.include_object_type = include_object_type
        self.allow_geometry_collection = allow_geometry_collection

    def _to_feature(self, feature_geometry, *, properties: dict[str, Any]):
        _properties = {}

        # _properties["id"] = ...?

        _properties |= dict_key_to_camel_case(properties)

        feat = Feature(
            geometry=feature_geometry,
            properties=_properties,
        )

        return feat

    def yield_feature(
        self,
        document: IRDocument,
    ):
        # lod = ["0", "1", "2"]

        for obj in document.city_objects:
            # NOTE: Get the geometry with the lowest LOD
            geom = next(filter(lambda x: x.lod == "0", obj.geometry), None)
            if geom is None:
                geom = next(filter(lambda x: x.lod == "1", obj.geometry), None)
            if geom is None:
                geom = next(filter(lambda x: x.lod == "2", obj.geometry), None)

            # if "0" in lod:
            #     geom = next(filter(lambda x: x.lod == "0", obj.geometry), None)
            # if "1" in lod:
            #     geom = next(filter(lambda x: x.lod == "1", obj.geometry), None)
            #     # raise NotImplementedError("LOD 1")
            # if "2" in lod:
            #     geom = next(filter(lambda x: x.lod == "2", obj.geometry), None)

            if geom is None:
                continue

            # WIP: exterior only; TODO: Fix this
            base_polygons = [surface[0] for surface in geom.boundaries]

            if self.altitude:
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

            # TODO: Make this optional
            properties["_gml_id"] = obj.id

            if self.include_object_type:
                properties["type"] = obj.type

            if len(polygons) == 1:
                feature = self._to_feature(polygons[0], properties=properties)
                # print(feature)
                yield feature
            else:
                if self.allow_geometry_collection:
                    feature = self._to_feature(
                        GeometryCollection(polygons), properties=properties
                    )
                    # print(feature)
                    yield feature
                else:
                    for polygon in polygons:
                        feature = self._to_feature(polygon, properties=properties)
                        # print(feature)
                        yield feature
                    # raise AssertionError("No geometry")


class GeoJSONWriter:
    def transform(
        self,
        document: IRDocument,
        *,
        altitude: bool = False,
        include_object_type: bool = False,
        seq: bool = False,
    ) -> list | dict:
        feature_generator = FeatureGenerator(
            altitude=altitude, include_object_type=include_object_type
        )

        if seq:
            lines = [feature for feature in feature_generator.yield_feature(document)]

            return lines

        else:
            features = [
                feature for feature in feature_generator.yield_feature(document)
            ]

            return FeatureCollection(features)

        # else:
        #     # raise NotImplementedError()
        #     vertices_map = VerticesMap()
        #     city_objects = {}

        #     for obj in document.city_objects:
        #         indexed_geometries = []

        #         for geometry in obj.geometry:
        #             indexed_geometry, vertices_map = self.get_indexed_geometry(
        #                 geometry, vertices_map
        #             )
        #             indexed_geometries.append(indexed_geometry)

        #         city_objects.update(
        #             {
        #                 obj.id: {
        #                     "type": obj.type,
        #                     "attributes": obj.attributes,
        #                     "geometry": [
        #                         {
        #                             "type": indexed_geometry.type,
        #                             "lod": indexed_geometry.lod,
        #                             "boundaries": indexed_geometry.boundaries,
        #                         }
        #                         for indexed_geometry in indexed_geometries
        #                     ],
        #                 }
        #             }
        #         )
        #     result = {
        #         "type": "CityJSON",
        #         "version": "2.0",
        #         "extensions": {},
        #         "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]},
        #         "metadata": {
        #             "referenceSystem": f"https://www.opengis.net/def/crs/EPSG/0/{document.metadata.epsg}",
        #         },
        #         "CityObjects": city_objects,
        #         "vertices": vertices_map.vertices,
        #         # "appearance": {},
        #         # "geometry-templates": {},
        #     }

        #     return result

    def write_to(
        self,
        document_or_readable,
        outfile: str,
        *,
        altitude: bool = False,
        include_object_type: bool = True,
        seq=False,
    ):
        import json

        if hasattr(document_or_readable, "read"):
            document = document_or_readable.read()
        else:
            document = document_or_readable

        result = self.transform(
            document,
            altitude=altitude,
            include_object_type=include_object_type,
            seq=seq,
        )

        # NOTE: Precision https://github.com/jazzband/geojson#default-and-custom-precision
        with open(outfile, "w") as f:
            if seq:
                for line in result:
                    f.write(
                        json.dumps(line, separators=(",", ":"), ensure_ascii=False)
                        + "\n"
                    )
            else:
                f.write(json.dumps(result, separators=(",", ":"), ensure_ascii=False))
