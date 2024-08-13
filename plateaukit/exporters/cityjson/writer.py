from typing import Any

from plateaukit.exporters.cityjson.vertices_map import VerticesMap
from plateaukit.readers.citygml.ir_models import IRDocument, IRGeometry, IRMetadata

# @dataclass
# class IndexedGeometry:
#     type: str
#     boundaries: list[Any]
#     lod: str | None = None


class CityJSONWriter:
    def _get_indexed_boundaries(self, geometry: IRGeometry, vertices_map: VerticesMap):
        """Get indexed boundaries from geometry."""

        # TODO: handling composite surface seriously
        # print("get_indexed_boundaries")
        # print("type", geometry.type)

        boundaries = geometry.boundaries
        indexed_boundaries: list[Any] = []  # TODO: typing

        if geometry.type == "MultiPoint":
            for point in geometry.boundaries:
                index = vertices_map.to_index(point)
                indexed_boundaries.append(index)
            return indexed_boundaries, vertices_map

        elif geometry.type == "MultiLineString":
            for line in geometry.boundaries:
                indexed_line = []
                for point in line:
                    index = vertices_map.to_index(point)
                    indexed_line.append(index)
                indexed_boundaries.append(indexed_line)
            return indexed_boundaries, vertices_map

        elif geometry.type in ["MultiSurface", "CompositeSurface"]:
            for surface in boundaries:
                # print("surface", surface)
                indexed_surface = []
                for region in surface:
                    # print("region", region)

                    # NOTE: Reverse the order of vertices; this is necessary for
                    # being rendered correctly in cityjson-threejs-loader
                    # for SOME datasets
                    # eg. plateau-13213-higashimurayama-shi-2020
                    ## region = region[::-1]

                    indexed_region = []
                    unclosed_region = region[:-1]
                    for point in unclosed_region:
                        index = vertices_map.to_index(point)
                        indexed_region.append(index)
                    indexed_surface.append(indexed_region)
                indexed_boundaries.append(indexed_surface)
            # print("indexed_boundaries", indexed_boundaries, "aaa" * 100)
            return indexed_boundaries, vertices_map

        elif geometry.type == "Solid":
            for shell in boundaries:
                # print("shell", shell)
                indexed_shell = []
                for surface in shell:
                    indexed_surface = []
                    for region in surface:
                        # print("region", region)
                        indexed_region: list[int] = []
                        unclosed_region = region[:-1]
                        for point in unclosed_region:
                            # print("point", point)
                            index = vertices_map.to_index(point)
                            indexed_region.append(index)
                        # print("indexed_region", indexed_region)
                        indexed_surface.append(indexed_region)
                    indexed_shell.append(indexed_surface)
                indexed_boundaries.append(indexed_shell)
            # print("indexed_boundaries", indexed_boundaries)
            return indexed_boundaries, vertices_map
        else:
            raise NotImplementedError()

        # TODO: MultiSolid, CompositeSolid

        # for surface in exterior:
        #     unclosed_surface = surface[:-1]
        #     # print("unclosed_surface", unclosed_surface)
        #     single_exterior_surface_exterior = []

        #     for chunk in unclosed_surface:
        #         index = vertices_map.to_index(chunk)
        #         single_exterior_surface_exterior.append(index)

        #     indexed_surface = [single_exterior_surface_exterior]
        #     indexed_surfaces.append(indexed_surface)

        # return indexed_surfaces, vertices_map

    def get_indexed_geometry(self, geometry: IRGeometry, vertices_map: VerticesMap):
        """Convert geometries to an indexed geometry with a vertices map."""

        indexed_boundaries, vertices_map = self._get_indexed_boundaries(
            geometry,
            vertices_map,
        )

        indexed_geometry = IRGeometry(
            type=geometry.type,
            lod=geometry.lod,
            boundaries=indexed_boundaries,
            semantics=geometry.semantics,
        )

        return indexed_geometry, vertices_map

    def _get_meta(self, metadata: IRMetadata) -> dict:
        return {
            "type": "CityJSON",
            "version": "2.0",
            # "extensions": {},
            "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]},
            "metadata": {
                "referenceSystem": f"https://www.opengis.net/def/crs/EPSG/0/{metadata.epsg}",
            },
            "vertices": [],
            # "appearance": {},
            # "geometry-templates": {},
        }

    def transform(
        self,
        document: IRDocument,
        *,
        seq=False,
    ) -> list | dict:
        if seq:
            lines = []
            cj_meta = self._get_meta(document.metadata)
            lines.append(cj_meta)

            for obj in document.city_objects:
                indexed_geometries = []
                vertices_map = VerticesMap()

                if obj.geometry is None:
                    pass
                else:
                    for geometry in obj.geometry:
                        indexed_geometry, vertices_map = self.get_indexed_geometry(
                            geometry, vertices_map
                        )
                        indexed_geometries.append(indexed_geometry)

                result = {
                    "type": "CityJSONFeature",
                    "CityObjects": {
                        obj.id: {
                            "type": obj.type,
                            "attributes": obj.attributes,
                            "geometry": [
                                {
                                    "type": indexed_geometry.type,
                                    "lod": indexed_geometry.lod,
                                    "boundaries": indexed_geometry.boundaries,
                                }
                                for indexed_geometry in indexed_geometries
                            ],
                        }
                    },
                    "vertices": vertices_map.vertices,
                    # "appearance": {},
                    # "geometry-templates": {},
                }
                lines.append(result)

            return lines

        else:
            # raise NotImplementedError()
            vertices_map = VerticesMap()
            city_objects = {}

            for obj in document.city_objects:
                indexed_geometries = []

                for geometry in obj.geometry:
                    indexed_geometry, vertices_map = self.get_indexed_geometry(
                        geometry, vertices_map
                    )
                    indexed_geometries.append(indexed_geometry)

                city_objects.update(
                    {
                        obj.id: {
                            "type": obj.type,
                            "attributes": obj.attributes,
                            "geometry": [
                                {
                                    "type": indexed_geometry.type,
                                    "lod": indexed_geometry.lod,
                                    "boundaries": indexed_geometry.boundaries,
                                }
                                for indexed_geometry in indexed_geometries
                            ],
                        }
                    }
                )
            result = {
                "type": "CityJSON",
                "version": "2.0",
                "extensions": {},
                "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]},
                "metadata": {
                    "referenceSystem": f"https://www.opengis.net/def/crs/EPSG/0/{document.metadata.epsg}",
                },
                "CityObjects": city_objects,
                "vertices": vertices_map.vertices,
                # "appearance": {},
                # "geometry-templates": {},
            }

            return result

    def write_to(
        self,
        document_or_readable,
        outfile: str,
        *,
        seq=False,
    ):
        import json

        if hasattr(document_or_readable, "read"):
            document = document_or_readable.read()
        else:
            document = document_or_readable

        result = self.transform(document, seq=seq)

        with open(outfile, "w") as f:
            if seq:
                for line in result:
                    f.write(
                        json.dumps(line, separators=(",", ":"), ensure_ascii=False)
                        + "\n"
                    )
            else:
                f.write(json.dumps(result, separators=(",", ":"), ensure_ascii=False))
