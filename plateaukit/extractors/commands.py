import concurrent.futures
from multiprocessing import Manager
from pathlib import Path

from lxml import etree
from tortoise import Tortoise
from tqdm import tqdm

from plateaukit import db
from plateaukit.constants import nsmap
from plateaukit.extractors.utils import (extract_gml_id, extract_name,
                                      extract_string_attribute_value)
from plateaukit.models import Entity


# TODO: List all attribute names
def list_properties(infiles, outfile):
    for infile in infiles:
        with open(infile, "r") as f:
            tree = etree.parse(f)
            print(dir(tree))
            for i, el in enumerate(
                tree.iterfind(f"./{nsmap['core']}cityObjectMember/*")
            ):
                print(list(el))
                if i > 1:
                    break
            # for el in tree.iterfind("./core:CityModel/*"):
            #     print(el)


# async def extract_properties_single(infile):
#     await Tortoise.init(
#         db_url=DB_URL, modules={"models": ["plateaukit.models"]}
#     )

#     async with in_transaction() as connection:
#         with open(infile, "r") as f:
#             tree = etree.parse(f)
#             for i, el in enumerate(
#                 tree.iterfind(f"./{nsmap['core']}cityObjectMember/*")
#             ):
#                 building_id = extract_string_attribute_value(el, "建物ID")
#                 name = extract_name(el)
#                 # tqdm.write(f"{building_id} {name}")

#                 try:
#                     entity = Entity(ns="plateau", uid=building_id, name=name)
#                     await entity.save(using_db=connection)
#                     # print(entity)
#                 except tortoise.exceptions.IntegrityError as err:
#                     # print(err)
#                     pass


def extract_properties_single_with_quit(infile, quit):
    entities = []

    with open(infile, "r") as f:
        tree = etree.parse(f)
        for i, el in enumerate(tree.iterfind(f"./{nsmap['core']}cityObjectMember/*")):
            # building_id = extract_string_attribute_value(el, "建物ID")
            building_id = extract_gml_id(el)
            name = extract_name(el)
            # tqdm.write(f"{building_id} {name}")

            entity = Entity(ns="plateau", uid=building_id, name=name)
            entities.append(entity)

    return entities


async def extract_properties(infiles, db_filename):
    db_filename = Path(db_filename).resolve()
    DB_URL = "sqlite://{}".format(db_filename)

    if not Path(db_filename).exists():
        await db.init(DB_URL)

    await Tortoise.init(db_url=DB_URL, modules={"models": ["plateaukit.models"]})

    with Manager() as manager:
        quit = manager.Event()
        with concurrent.futures.ProcessPoolExecutor(max_workers=None) as pool:
            futures = []
            for i, infile in enumerate(infiles):
                futures.append(pool.submit(extract_properties_single_with_quit, infile, quit))
            with tqdm(concurrent.futures.as_completed(futures), total=len(futures)) as pbar:
                try:
                    for future in pbar:
                        entities = future.result()
                        await Entity.bulk_create(entities)
                except KeyboardInterrupt:
                    quit.set()
                    pool.shutdown(wait=True, cancel_futures=True)
                    # pool._processes.clear()
                    # concurrent.futures.thread._threads_queues.clear()
                    raise

