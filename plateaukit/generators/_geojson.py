import concurrent.futures
import math
import sys
from multiprocessing import Manager
from pathlib import Path

import geojson
import pyproj
from geojson import Feature, FeatureCollection, GeometryCollection, Polygon
from loguru import logger
from lxml import etree
from tqdm.auto import tqdm

from plateaukit import extractors, utils
from plateaukit.constants import nsmap

logger.remove()
logger.add(sys.stderr, level="INFO")


def geojson_from_gml_single(
    infile,
    target_epsg=4326,  # WGS
    altitude=False,
    lod=[0],
    attributes=["measuredHeight"],
    allow_geometry_collection=False,
):
    logger.debug(infile)

    tree = etree.parse(infile)

    src_epsg = extractors.utils.extract_epsg(tree)  # 6697
    logger.debug(src_epsg)
    crs_orig = pyproj.CRS(src_epsg)
    logger.debug(repr(crs_orig))

    logger.debug(f"EPSG:{src_epsg} → EPSG:{target_epsg}")

    transformer = pyproj.Transformer.from_crs(src_epsg, target_epsg)

    features = []

    for i, el in enumerate(tree.iterfind(f"./{nsmap['core']}cityObjectMember/*")):
        # print(el)
        # building_id = extract.utils.extract_string_attribute_value(el, "建物ID")
        try:
            building_id = extractors.utils.extract_gml_id(el)
        except Exception as err:
            logger.error(err)
            building_id = None
        # name = extract.utils.extract_name(el)
        # print(building_id)
        # tqdm.write(f"{building_id} {name}")
        # entity = Entity(ns="plateau", uid=building_id, name=name)
        # entities.append(entity)

        ## Attributes
        attribute_values = None
        if attributes:
            attribute_values = {}
            for attribute in attributes:
                value = extractors.utils.exract_bldg_attribute(el, attribute)
                # TODO: fix
                try:
                    value = float(value) if value else None
                except:
                    pass
                attribute_values[attribute] = value

        ## EXTRACT LODs
        if len(lod) > 1:
            raise NotImplementedError("too many LOD values")

        if 0 in lod:
            poslists = extractors.utils.extract_lod0_poslists(el)
            # print(lod0_poslist)
        if 1 in lod:
            try:
                poslists = extractors.utils.extract_lod1_poslists(el)
            except Exception as err:
                logger.error(err)
                poslists = []

        polygons = []

        for poslist in poslists:
            chunked = utils.chunker(poslist, 3)

            base_polygon = [transformer.transform(*coord) for coord in chunked]

            # print(list(utils.chunker(lod0_poslist, 3)))
            # print(base_polygon)

            if altitude:
                # raise NotImplementedError()
                base_polygon = list(map(lambda x: [x[1], x[0], x[2]], base_polygon))
            else:
                base_polygon = list(map(lambda x: [x[1], x[0]], base_polygon))

            poly = Polygon([base_polygon])
            # print(poly)

            polygons.append(poly)

        def to_feature(feature_geometry):
            properties = {}
            if building_id:
                properties["id"] = building_id
            if attributes:
                properties |= attribute_values

            feat = Feature(
                geometry=feature_geometry,
                properties=properties,
            )
            # print(feat)

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


def geojson_from_gml_serial_with_quit(
    infiles,
    outfile,
    quit,
    **opts,
):
    features = []

    with tqdm(infiles) as pbar:
        for infile in pbar:
            logger.debug(infile)
            with open(infile, "r") as f:
                collection = geojson_from_gml_single(f, **opts)
                features.extend(collection["features"])
            if quit.is_set():
                return

    collection = FeatureCollection(features)

    # NOTE: Precision https://github.com/jazzband/geojson#default-and-custom-precision
    with open(outfile, "w") as f:
        geojson.dump(collection, f, ensure_ascii=False, separators=(",", ":"))


def geojson_from_gml(infiles, outfile, split, **opts):
    group_size = math.ceil(len(infiles) / split)
    logger.debug(f"GMLs per GeoJSON: {group_size}")
    infile_groups = utils.chunker(infiles, group_size)

    with Manager() as manager:
        quit = manager.Event()
        with concurrent.futures.ProcessPoolExecutor(max_workers=None) as pool:
            futures = []
            for i, infile_group in enumerate(infile_groups):
                stem = Path(outfile).stem
                if split > 1:
                    group_outfile = Path(outfile).with_stem(f"{stem}.{i + 1}")
                else:
                    group_outfile = outfile
                futures.append(
                    pool.submit(
                        geojson_from_gml_serial_with_quit,
                        infile_group,
                        group_outfile,
                        quit,
                        **opts,
                    )
                )
            with tqdm(
                concurrent.futures.as_completed(futures), total=len(futures)
            ) as pbar:
                try:
                    for future in pbar:
                        result = future.result()
                except KeyboardInterrupt:
                    quit.set()
                    pool.shutdown(wait=True, cancel_futures=True)
                    # pool._processes.clear()
                    # concurrent.futures.thread._threads_queues.clear()
                    raise
