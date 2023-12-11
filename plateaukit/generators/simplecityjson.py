import concurrent.futures
import io
import json
import math
import os.path
from decimal import Decimal
from multiprocessing import Manager
from os import PathLike
from pathlib import Path

from bidict import bidict
from fs import open_fs
from rich.progress import Progress

from plateaukit import parallel, utils
from plateaukit.logger import logger
from plateaukit.parsers import CodelistParser, PLATEAUCityGMLParser
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


def get_indexed_lod1_solid(city_obj, vertices_map: VerticesMap):
    # TODO: handling composite surface seriously
    # print("get_indexed_lod1_solid")

    geom = next(
        filter(lambda x: x["lod"] == 1 and x["type"] == "Solid", city_obj.geometry),
        None,
    )

    # print("geom", geom)

    indexed_surfaces = []

    exterior = geom["boundaries"][0]

    # print("exterior", exterior)

    for surface in exterior:
        unclosed_surface = surface[:-1]
        # print("unclosed_surface", unclosed_surface)
        single_exterior_surface_exterior = []

        for chunk in unclosed_surface:
            index = vertices_map.to_index(chunk)
            single_exterior_surface_exterior.append(index)

        indexed_surface = [single_exterior_surface_exterior]
        indexed_surfaces.append(indexed_surface)

    return indexed_surfaces, vertices_map


def get_indexed_boundaries(geometry, vertices_map: VerticesMap):
    # TODO: handling composite surface seriously
    # print("get_indexed_boundaries")
    # print("type", geometry["type"])

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
        for surface in geometry["boundaries"]:
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
        for shell in geometry["boundaries"]:
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


# def parse_lod2solid(element_cityObject, vertices_map: VerticesMap):
#     # TODO: handling composite surface seriously
#     elem_compositeSurface = element_cityObject.find(
#         f"./{nsmap['bldg']}lod2Solid/{nsmap['gml']}Solid/{nsmap['gml']}exterior/{nsmap['gml']}CompositeSurface"
#     )
#     # print(elem_compositeSurface)

#     elems_surfaceMember = elem_compositeSurface.iterfind(
#         f".//{nsmap['gml']}surfaceMember"
#     )

#     hrefs = []
#     for elem in elems_surfaceMember:
#         # print(elem)
#         href = elem.get(f"{nsmap['xlink']}href")
#         # Remove hash
#         href = href[1:]
#         # print(href)
#         hrefs.append(href)

#     elems_member = []

#     # Collect linked elements
#     for href in hrefs:
#         # NOTE: this may not be guaranteed
#         elem = element_cityObject.find(f".//*[@{nsmap['gml']}id='{href}']")
#         # print(elem)
#         elems_member.append(elem)

#     exterior_surfaces = []

#     for elem in elems_member:
#         els_list = elem.iterfind(f".//{nsmap['gml']}posList")
#         for el in els_list:
#             text = el.text
#             chunks = parse_posList(text)
#             logger.debug(chunks)
#             single_exterior_surface_exterior = []
#             for chunk in chunks:
#                 index = vertices_map.to_index(chunk)
#                 single_exterior_surface_exterior.append(index)
#             single_exterior_surface = [single_exterior_surface_exterior]
#             exterior_surfaces.append(single_exterior_surface)

#     return exterior_surfaces, vertices_map


class CityJSONConverter:
    def __init__(self, target_epsg):
        self.target_epsg = target_epsg

        self.vertices_map = VerticesMap()

    # @streamable_dict
    def generate_city_object(
        self,
        infiles: list[str],
        object_types: list[str] | None,
        lod: list[int],
        codelist_infiles: list[str] | None = None,
        zipfile: str | PathLike | None = None,
        task_id=None,
        quit=None,
        _progress=None,
    ):
        # vertices_map = VerticesMap()

        # Load codelists
        codelist_file_map = None

        if codelist_infiles and infiles:
            base_path = Path(infiles[0]).parent  # TODO: Fix this
            codelist_file_map = dict()

            for codelist_infile in codelist_infiles:
                if zipfile is not None:
                    with open_fs(f"zip://{zipfile}") as zip_fs:
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

            if zipfile is not None:
                with open_fs(f"zip://{zipfile}") as zip_fs:
                    with zip_fs.open(infile, "r") as f:
                        citygml = parser.parse(f)
            else:
                with open(infile, "r") as f:
                    # print(f"infile: {infile}")

                    citygml = parser.parse(f)

            for city_obj in citygml.city_objects:
                if quit and quit.is_set():
                    return

                # print("city_obj", city_obj)

                if object_types is not None and city_obj.type not in object_types:
                    continue

                indexed_geoms = []

                for geom in city_obj.geometry:
                    if geom["lod"] not in lod:
                        continue

                    # print("geom", geom)
                    boundaries, vertices_map = get_indexed_boundaries(
                        geom, self.vertices_map
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
                    "attributes": dict_key_to_camel_case(city_obj.attributes),
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


def cityson_from_gml_serial_with_quit(
    infiles,
    outfile,
    object_types,
    lod,
    codelist_infiles,
    zipfile=None,
    task_id=None,
    quit=None,
    _progress=None,
    **opts,
):
    # TODO: logger does not work; must use QueueHandler
    logger.debug("[*] cityson_from_gml_serial_with_quit")

    target_epsg = 3857
    # target_epsg = 4326

    converter = CityJSONConverter(target_epsg=target_epsg)

    city_objects = dict(
        converter.generate_city_object(
            infiles,
            object_types=object_types,
            lod=lod,
            codelist_infiles=codelist_infiles,
            zipfile=zipfile,
            task_id=task_id,
            quit=quit,
            _progress=_progress,
        )
    )

    # print(city_objects)

    # vertices = [
    #     transformer.transform(*vertice) for vertice in converter.vertices_map.vertices
    # ]
    vertices = converter.vertices_map.vertices

    result = {
        "type": "CityJSON",
        "version": "2.0",
        "extensions": {},
        "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]},
        "metadata": {
            "referenceSystem": f"https://www.opengis.net/def/crs/EPSG/0/{target_epsg}",
        },
        "CityObjects": city_objects,
        "vertices": vertices,
        # "appearance": {},
        # "geometry-templates": {},
    }
    # result_debug = json.dumps(result, indent=2, ensure_ascii=False)
    # print(result_debug)

    with open(outfile, "w") as f:
        json.dump(result, f, ensure_ascii=False, separators=(",", ":"))

    total = len(infiles) + 1  # + 1 for geojson.dump

    # Complete the progress bar
    _progress[task_id] = {"progress": total, "total": total}


def cityjson_from_citygml(
    infiles,
    outfile,
    split: int = 1,
    zipfile=None,
    precision=16,
    object_types=None,
    lod: list[int] = [1, 2],
    codelist_infiles=None,
    progress={},
):
    logger.debug("[*] cityjson_from_citygml")
    # vertices_map = VerticesMap()
    # city_objects = {}

    group_size = math.ceil(len(infiles) / split)
    logger.debug(f"GMLs per GeoJSON: {group_size}")
    infile_groups = utils.chunker(infiles, group_size)

    with Progress() as rprogress:
        overall_progress_description = progress.get("description", "Processing...")
        overall_task_id = rprogress.add_task(overall_progress_description)

        with Manager() as manager:
            quit = manager.Event()
            _progress = manager.dict()

            with concurrent.futures.ProcessPoolExecutor(max_workers=None) as pool:
                futures = []
                futures_status = dict()
                for i, infile_group in enumerate(infile_groups):
                    stem = Path(outfile).stem

                    if split > 1:
                        group_outfile = Path(outfile).with_stem(f"{stem}.{i + 1}")
                    else:
                        group_outfile = outfile

                    task_id = rprogress.add_task(
                        f"[cyan]Progress #{i + 1}", total=len(infile_group)
                    )
                    # task_id = None

                    logger.debug(f"group_outfile: {group_outfile}")

                    future = pool.submit(
                        cityson_from_gml_serial_with_quit,
                        infile_group,
                        group_outfile,
                        object_types=object_types,
                        lod=lod,
                        codelist_infiles=codelist_infiles,
                        zipfile=zipfile,
                        task_id=task_id,
                        _progress=_progress,
                        quit=quit,
                        # **kwargs,
                    )

                    futures.append(future)
                    futures_status[future] = {
                        "task_id": task_id,
                        "counter": i + 1,
                        "failed": False,
                    }

                parallel.wait_futures(
                    futures,
                    pool,
                    quit,
                    futures_status,
                    overall_progress={
                        "task_id": overall_task_id,
                        "description": overall_progress_description,
                    },
                    rich_progress=rprogress,
                    shared_progress_status=_progress,
                )

                # try:
                #     while (
                #         n_finished := sum([future.done() for future in futures])
                #     ) < len(futures):
                #         rprogress.update(
                #             overall_task_id,
                #             completed=n_finished,
                #             total=len(futures),
                #         )
                #         for task_id, status in _progress.items():
                #             latest = status["progress"]
                #             total = status["total"]

                #             rprogress.update(
                #                 task_id,
                #                 completed=latest,
                #                 total=total,
                #                 visible=latest < total,
                #             )

                #     # Finish up the overall progress bar
                #     rprogress.update(
                #         overall_task_id,
                #         completed=n_finished,
                #         total=len(futures),
                #         description="[green]Done",
                #     )

                # except KeyboardInterrupt:
                #     quit.set()
                #     pool.shutdown(wait=True, cancel_futures=True)
                #     # pool._processes.clear()
                #     # concurrent.futures.thread._threads_queues.clear()
                #     raise
