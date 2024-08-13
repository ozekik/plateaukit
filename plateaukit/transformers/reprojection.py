import pyproj

from plateaukit.readers.citygml.ir_models import IRDocument, IRGeometry
from plateaukit.readers.citygml.reader import Readable

from .geometry import GeometryTransformer

BOUNDARIES_DEPTH_MAPPING = {
    "MultiPoint": 1,
    "MultiLineString": 2,
    "MultiSurface": 3,
    "CompositeSurface": 3,
    "Solid": 4,
    "MultiSolid": 5,
    "CompositeSolid": 5,
}


class ReprojectionTransformer(GeometryTransformer):
    def __init__(
        self,
        *,
        target_epsg: int,
    ):
        self.target_epsg = target_epsg

    def _reproject_geometry(self, geometry: IRGeometry):
        depth = BOUNDARIES_DEPTH_MAPPING.get(geometry.type, None)

        if depth is None:
            raise ValueError(f"Unsupported geometry type: {geometry.type}")

        # TODO: Type checking
        if depth == 1:
            new_bounds = list(self.transformer.itransform(geometry.boundaries))
        elif depth == 2:
            new_bounds = [
                list(self.transformer.itransform(bounds))
                for bounds in geometry.boundaries
            ]
        elif depth == 3:
            new_bounds = [
                [list(self.transformer.itransform(bounds)) for bounds in surface]
                for surface in geometry.boundaries
            ]
        elif depth == 4:
            new_bounds = [
                [
                    [list(self.transformer.itransform(bounds)) for bounds in region]
                    for region in surface
                ]
                for surface in geometry.boundaries
            ]
        elif depth == 5:
            new_bounds = [
                [
                    [
                        [list(self.transformer.itransform(bounds)) for bounds in solid]
                        for solid in composite
                    ]
                    for composite in geometry.boundaries
                ]
            ]
        else:
            raise ValueError(f"Invalid depth: {depth}")

        geometry.boundaries = new_bounds

        return geometry

    def transform(self, readable: Readable):
        readable.transformers.append(self)

        return readable

    def transform_document(self, document: IRDocument):
        origin_epsg = document.metadata.epsg  # TODO: Check this

        self.transformer = pyproj.Transformer.from_crs(origin_epsg, self.target_epsg)

        for city_object in document.city_objects:
            for i, geom in enumerate(city_object.geometry):
                city_object.geometry[i] = self._reproject_geometry(geom)

        document.metadata.epsg = self.target_epsg

        return document
