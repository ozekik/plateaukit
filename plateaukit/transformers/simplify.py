import fast_simplification
import numpy as np

from plateaukit.exporters.cityjson.vertices_map import VerticesMap
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


class SimplifyTransformer(GeometryTransformer):
    def __init__(
        self,
        *,
        target_reduction: float,
    ):
        self.target_reduction = target_reduction

    def _simplify_geometry(self, geometry: IRGeometry):
        depth = BOUNDARIES_DEPTH_MAPPING.get(geometry.type, None)

        if depth is None:
            raise ValueError(f"Unsupported geometry type: {geometry.type}")

        vertices_map = VerticesMap()

        # TODO: Type checking
        # if depth == 1:
        #     new_bounds = list(self.transformer.itransform(geometry.boundaries))
        # elif depth == 2:
        #     new_bounds = [
        #         list(self.transformer.itransform(bounds))
        #         for bounds in geometry.boundaries
        #     ]
        if depth == 3:
            faces = []
            for surface in geometry.boundaries:
                for bounds in surface:
                    face = [vertices_map.to_index(vertex) for vertex in bounds]
                    faces.append(face)

            vertices = vertices_map.vertices

            vertices_out, faces_out = fast_simplification.simplify(
                vertices, faces, self.target_reduction, verbose=True
            )

            faces = np.array([[vertices_out[i] for i in face] for face in faces_out])

            new_bounds = [[face.tolist()] for face in faces]
        # elif depth == 4:
        #     new_bounds = [
        #         [
        #             [list(self.transformer.itransform(bounds)) for bounds in region]
        #             for region in surface
        #         ]
        #         for surface in geometry.boundaries
        #     ]
        # elif depth == 5:
        #     new_bounds = [
        #         [
        #             [
        #                 [list(self.transformer.itransform(bounds)) for bounds in solid]
        #                 for solid in composite
        #             ]
        #             for composite in geometry.boundaries
        #         ]
        #     ]
        else:
            raise ValueError(f"Invalid depth: {depth}")

        geometry.boundaries = new_bounds

        return geometry

    def transform(self, readable: Readable):
        readable.transformers.append(self)

        return readable

    def transform_document(self, document: IRDocument):
        for city_object in document.city_objects:
            for i, geom in enumerate(city_object.geometry):
                city_object.geometry[i] = self._simplify_geometry(geom)

        return document
