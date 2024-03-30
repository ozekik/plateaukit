import io
import os.path
from os import PathLike
from pathlib import Path
from typing import Any, Generator

from bidict import bidict
from fs import open_fs

from plateaukit.formats.citygml import PLATEAUCityGMLParser
from plateaukit.utils import dict_key_to_camel_case

# from json_stream import streamable_dict


class VerticesMap:
    counter: int
    index_by_vertex: bidict

    def __init__(self):
        self.counter = 0
        self.index_by_vertex = bidict()

    def to_index(self, vertex):
        if vertex not in self.index_by_vertex:
            self.index_by_vertex[vertex] = self.counter
            self.counter += 1
        return self.index_by_vertex[vertex]

    # def to_vertex(self, index):
    #     return self.index_by_vertex.inverse[index]

    # def exists_index(self, index):
    #     return index in self.index_by_vertex.inverse

    @property
    def vertices(self):
        return list(self.index_by_vertex.keys())

    def __contains__(self, vertex):
        return vertex in self.index_by_vertex


def _get_nesting_level(l):
    if isinstance(l, list):
        return 1 + max([_get_nesting_level(x) for x in l])
    else:
        return 0


def _get_min_z(boundaries: list):
    level = _get_nesting_level(boundaries)

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


def _shift_to_ground(boundaries: list, min_z: float):
    level = _get_nesting_level(boundaries)

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


def get_indexed_boundaries(
    geometry, vertices_map: VerticesMap, min_z: float | None = None
):
    # TODO: handling composite surface seriously
    # print("get_indexed_boundaries")
    # print("type", geometry["type"])

    boundaries = geometry["boundaries"]
    indexed_boundaries = []

    if geometry["type"] == "MultiPoint":
        for point in geometry["boundaries"]:
            index = vertices_map.to_index(point)
            indexed_boundaries.append(index)
        return indexed_boundaries, vertices_map

    elif geometry["type"] == "MultiLineString":
        for line in geometry["boundaries"]:
            indexed_line = []
            for point in line:
                index = vertices_map.to_index(point)
                indexed_line.append(index)
            indexed_boundaries.append(indexed_line)
        return indexed_boundaries, vertices_map

    elif geometry["type"] in ["MultiSurface", "CompositeSurface"]:
        if min_z:
            boundaries = _shift_to_ground(geometry["boundaries"], min_z)
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

    elif geometry["type"] == "Solid":
        if min_z:
            boundaries = _shift_to_ground(geometry["boundaries"], min_z)
        for shell in boundaries:
            # print("shell", shell)
            indexed_shell = []
            for surface in shell:
                indexed_surface = []
                for region in surface:
                    # print("region", region)
                    indexed_region = []
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


class CityJSONConverter:
    def __init__(self, target_epsg: int):
        self.target_epsg = target_epsg

        self.vertices_map = VerticesMap()

    def get_meta(self):
        return {
            "type": "CityJSON",
            "version": "2.0",
            # "extensions": {},
            "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]},
            "metadata": {
                "referenceSystem": f"https://www.opengis.net/def/crs/EPSG/0/{self.target_epsg}",
            },
            "vertices": [],
            # "appearance": {},
            # "geometry-templates": {},
        }

    def features(
        self,
        infiles: list[str],
        *,
        object_types: list[str] | None,
        lod: list[int],
        ground: bool = False,
        codelist_infiles: list[str] | None = None,
        zipfile: str | PathLike | None = None,
        selection: list[str] | None = None,
        task_id=None,
        quit=None,
        _progress=None,
    ):
        object_iter = self.generate_city_object(
            infiles,
            object_types=object_types,
            lod=lod,
            ground=ground,
            codelist_infiles=codelist_infiles,
            zipfile=zipfile,
            selection=selection,
            task_id=task_id,
            quit=quit,
            _progress=_progress,
        )

        for obj_id, obj in object_iter:
            # vertices = [
            #     transformer.transform(*vertice) for vertice in converter.vertices_map.vertices
            # ]
            vertices = self.vertices_map.vertices

            result = {
                "type": "CityJSONFeature",
                "CityObjects": {obj_id: obj},
                "vertices": vertices,
                # "appearance": {},
                # "geometry-templates": {},
            }

            self.vertices_map = VerticesMap()

            yield result

    def convert(
        self,
        infiles: list[str],
        *,
        object_types: list[str] | None,
        lod: list[int],
        ground: bool = False,
        codelist_infiles: list[str] | None = None,
        zipfile: str | PathLike | None = None,
        selection: list[str] | None = None,
        task_id=None,
        quit=None,
        _progress=None,
    ):
        city_objects = dict(
            self.generate_city_object(
                infiles,
                object_types=object_types,
                lod=lod,
                ground=ground,
                codelist_infiles=codelist_infiles,
                zipfile=zipfile,
                selection=selection,
                task_id=task_id,
                quit=quit,
                _progress=_progress,
            )
        )

        # vertices = [
        #     transformer.transform(*vertice) for vertice in converter.vertices_map.vertices
        # ]
        vertices = self.vertices_map.vertices

        result = {
            "type": "CityJSON",
            "version": "2.0",
            "extensions": {},
            "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]},
            "metadata": {
                "referenceSystem": f"https://www.opengis.net/def/crs/EPSG/0/{self.target_epsg}",
            },
            "CityObjects": city_objects,
            "vertices": vertices,
            # "appearance": {},
            # "geometry-templates": {},
        }

        return result

    # @streamable_dict
    def generate_city_object(
        self,
        infiles: list[str],
        *,
        object_types: list[str] | None,
        lod: list[int],
        ground: bool = False,
        codelist_infiles: list[str] | None = None,
        zipfile: str | PathLike | None = None,
        selection: list[str] | None = None,
        task_id=None,
        quit=None,
        _progress=None,
    ) -> Generator[tuple[str | None, dict[str, Any]], None, None]:
        # vertices_map = VerticesMap()

        # Load codelists
        codelist_file_map = None

        if zipfile is not None:
            zip_fs = open_fs(f"zip://{zipfile}")
        else:
            zip_fs = None

        if codelist_infiles and infiles:
            base_path = Path(infiles[0]).parent  # TODO: Fix this
            codelist_file_map = dict()

            for codelist_infile in codelist_infiles:
                if zip_fs:
                    with zip_fs.open(codelist_infile, "rb") as f:
                        relative_path = os.path.relpath(codelist_infile, base_path)
                        codelist_file_map[relative_path] = io.BytesIO(f.read())
                else:
                    with open(codelist_infile, "rb") as f:
                        relative_path = os.path.relpath(codelist_infile, base_path)
                        codelist_file_map[relative_path] = io.BytesIO(f.read())

        parser = PLATEAUCityGMLParser(
            target_epsg=self.target_epsg, codelist_file_map=codelist_file_map
        )

        total = len(infiles) + 1  # + 1 for geojson.dump

        for i, infile in enumerate(infiles):
            if task_id is not None and _progress is not None:
                _progress[task_id] = {"progress": i + 1, "total": total}

            _open = zip_fs.open if zip_fs else open

            with _open(infile, "rb") as f:
                co_iter = parser.iterparse(f, selection=selection)
                for city_obj in co_iter:
                    if quit and quit.is_set():
                        return

                    # print("city_obj", city_obj)

                    if object_types is not None and city_obj.type not in object_types:
                        continue

                    indexed_geoms = []

                    if city_obj.geometry is not None:
                        min_z = None

                        if ground:
                            min_z = 0xFFFF
                            for geom in city_obj.geometry:
                                if geom["lod"] not in lod:
                                    continue

                                # print("geom", geom)
                                min_z = min(min_z, _get_min_z(geom["boundaries"]))
                            # print("min_z", min_z)

                        for geom in city_obj.geometry:
                            if geom["lod"] not in lod:
                                continue

                            # print("geom", geom)
                            boundaries, vertices_map = get_indexed_boundaries(
                                geom,
                                self.vertices_map,
                                min_z=min_z,
                            )

                            indexed_geom = dict(
                                geom, lod=str(geom["lod"]), boundaries=boundaries
                            )

                            # print("indexed_geom", indexed_geom)
                            indexed_geoms.append(indexed_geom)

                            self.vertices_map = vertices_map

                    # print("indexed_geoms", indexed_geoms)

                    # obj_id = city_obj.attributes.get("building_id", city_obj.id)
                    obj_id = city_obj.id

                    yield obj_id, {
                        "type": city_obj.type,  # TODO: There is no Track type etc. in CityJSON
                        "attributes": dict_key_to_camel_case(city_obj.attributes or {}),
                        # "attributes": {"建物ID": "13104-bldg-52530", "measuredHeight": 61.9},
                        # "children": [
                        #     "ID_22730c8f-9fbc-4d58-88dd-5569d7480fad",
                        #     "ID_598f2fab-030f-429c-b938-a222e04d8e4b",
                        #     "ID_db473977-e95e-4075-b0be-55eb65974610",
                        #     "ID_ac26b2cb-553e-428a-9f10-2659419e824d",
                        # ],
                        "geometry": indexed_geoms,
                        # [
                        # {
                        #     "type": "MultiSurface",
                        #     "lod": "0",
                        #     "boundaries": [],
                        # },
                        # {
                        #     "type": "Solid",
                        #     "lod": "1",
                        #     "boundaries": boundaries,
                        #     # "semantics": {
                        #     #     "surfaces": [],
                        #     #     "values": [],
                        #     # },
                        #     # "texture": {"rgbTexture": {"values": []}},
                        # },
                        # ],
                        # "address": [{"Country": "日本", "Locality": "東京都新宿区西新宿一丁目"}],
                    }

        if zip_fs:
            zip_fs.close()
