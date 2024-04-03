import pyproj
from lxml import etree

from plateaukit import utils
from plateaukit.formats.citygml.constants import default_nsmap

MAPLIBRE_SCALE_FACTOR = 10000000
MERCATOR_HALF_WORLD_LENGTH = 20037508.342789243906736373901367187500


Vector3 = tuple[float, float, float]
Point = Vector3


class GeometryParser:
    """A parser for CityGML geometries.

    Attributes:
        transformer: A pyproj.Transformer instance.
        maplibre: Whether to use MapLibre scale factor.
    """

    transformer: pyproj.Transformer | None
    maplibre: bool

    def __init__(
        self, transformer: pyproj.Transformer | None = None, maplibre: bool = False
    ):
        self.transformer = transformer
        self.maplibre = maplibre

    def _transform(
        self,
        vertices: list[Point],
        scale: Vector3 = (1, 1, 1),
        translate: Vector3 = (0, 0, 0),
    ) -> list[Point]:
        # TODO: numpy

        transformed = []

        for vertex in vertices:
            x, y, z = vertex
            nx = (x * scale[0]) + translate[0]
            ny = (y * scale[1]) + translate[1]
            nz = (z * scale[2]) + translate[2]
            transformed.append((nx, ny, nz))

        return transformed

    def _adjust_mercator_to_maplibre(self, vertices):
        xy = -(0.5 * MAPLIBRE_SCALE_FACTOR) / MERCATOR_HALF_WORLD_LENGTH
        z = 0.5 * MAPLIBRE_SCALE_FACTOR / MERCATOR_HALF_WORLD_LENGTH
        scale = (xy, xy, z)

        transformed = self._transform(
            vertices,
            scale=scale,
            translate=(
                0.5 * MAPLIBRE_SCALE_FACTOR,
                0.5 * MAPLIBRE_SCALE_FACTOR,
                0,
            ),
        )

        return transformed

    def extract_chunked_poslists(self, root: etree._Element):
        path = "/".join(
            [
                ".//gml:surfaceMember",  # TODO: Check this
                "gml:Polygon",
                "gml:exterior",
                "gml:LinearRing",
                "gml:posList",
            ]
        )
        # print(path)
        # results = root.findall(path, nsmap)

        parsed = []

        for result in root.iterfind(path, default_nsmap):
            # TODO: Handle cases where result.text is None
            text = result.text.strip()
            poslist = map(float, text.split(" "))

            chunked = list(utils.chunker(poslist, 3))

            if self.maplibre and self.transformer:
                chunked = list(self.transformer.itransform(chunked))
                chunked = self._adjust_mercator_to_maplibre(chunked)
            elif self.transformer:
                chunked = list(self.transformer.itransform(chunked))

            surface = [chunked]
            parsed.append(surface)

        return parsed
