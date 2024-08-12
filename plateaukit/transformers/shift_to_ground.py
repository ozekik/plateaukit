from plateaukit.readers.citygml.ir_models import IRDocument

from .geometry import GeometryTransformer


class ShiftToGroundTransformer(GeometryTransformer):
    def _get_nesting_level(self, boundaries: list | None):
        if isinstance(boundaries, list):
            return 1 + max([self._get_nesting_level(x) for x in boundaries])
        else:
            return 0

    def _get_min_z(self, boundaries: list):
        level = self._get_nesting_level(boundaries)

        # Nest level 3
        if level == 3:
            min_z = min(
                [
                    min([min([point[2] for point in region]) for region in surface])
                    for surface in boundaries
                ]
            )
        # Nest level 4
        elif level == 4:
            min_z = min(
                [
                    min(
                        [
                            min([min([point[2] for point in shell]) for shell in solid])
                            for solid in surface
                        ]
                    )
                    for surface in boundaries
                ]
            )
        else:
            raise NotImplementedError()

        return min_z

    def _shift_boundaries_to_ground(self, boundaries: list, min_z: float):
        level = self._get_nesting_level(boundaries)

        # Nest level 3
        if level == 3:
            boundaries = [
                [
                    [(point[0], point[1], point[2] - min_z) for point in region]
                    for region in surface
                ]
                for surface in boundaries
            ]
        # Nest level 4
        elif level == 4:
            boundaries = [
                [
                    [
                        [(point[0], point[1], point[2] - min_z) for point in shell]
                        for shell in solid
                    ]
                    for solid in surface
                ]
                for surface in boundaries
            ]

        return boundaries

    def transform_document(self, document: IRDocument):
        for city_object in document.city_objects:
            min_z = 0xFFFF

            for geometry in city_object.geometry:
                min_z = min(min_z, self._get_min_z(geometry.boundaries))
                geometry.boundaries = self._shift_boundaries_to_ground(
                    geometry.boundaries, min_z
                )

        return document
