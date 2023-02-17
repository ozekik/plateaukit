import json
from decimal import Decimal

from lxml import etree
from loguru import logger
from bidict import bidict

from plateaukit.constants import nsmap
from plateaukit.utils import parse_posList


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


def cityjson_from_gml_lod1(infiles, precision=16):
    counter = 0
    vertices = []

    for infile in infiles:
        with open(infile, "r") as f:
            tree = etree.parse(f)
            tree = tree.find(
                f".//{nsmap['bldg']}Building[@{nsmap['gml']}id='BLD_ffc04e24-60a0-48ce-8b20-93a51c160bb3']"
            )
            print(tree)

            lod1solid_tree = tree.find(f"./{nsmap['bldg']}lod1Solid")
            print(lod1solid_tree)

            # TODO: handling composite surface seriously
            compositeSurface_tree = lod1solid_tree.find(
                f"./{nsmap['gml']}Solid/{nsmap['gml']}exterior/{nsmap['gml']}CompositeSurface"
            )
            print(compositeSurface_tree)

            posLists = compositeSurface_tree.iterfind(
                f".//{nsmap['gml']}exterior/{nsmap['gml']}LinearRing/{nsmap['gml']}posList"
            )

            exterior_surfaces = []

            for posList in posLists:
                text = posList.text
                chunks = parse_posList(text)
                single_exterior_surface_exterior = []
                for chunk in chunks:
                    vertices.append(chunk)
                    single_exterior_surface_exterior.append(counter)
                    counter += 1
                single_exterior_surface = [single_exterior_surface_exterior]
                exterior_surfaces.append(single_exterior_surface)

            print(exterior_surfaces)

            result = {
                "type": "CityJSON",
                "version": "1.1",
                "extensions": {},
                "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]},
                "metadata": {},
                "CityObjects": {
                    "BLD_f51c1fff-5198-4196-ac9b-39a5c1e48dca": {
                        "type": "Building",
                        # "attributes": {"建物ID": "13104-bldg-52530", "measuredHeight": 61.9},
                        # "children": [
                        #     "ID_22730c8f-9fbc-4d58-88dd-5569d7480fad",
                        #     "ID_598f2fab-030f-429c-b938-a222e04d8e4b",
                        #     "ID_db473977-e95e-4075-b0be-55eb65974610",
                        #     "ID_ac26b2cb-553e-428a-9f10-2659419e824d",
                        # ],
                        "geometry": [
                            # {
                            #     "type": "MultiSurface",
                            #     "lod": "0",
                            #     "boundaries": [],
                            # },
                            {
                                "type": "Solid",
                                "lod": "2",
                                "boundaries": [
                                    # Exterior shell
                                    exterior_surfaces,
                                    # Interior shells
                                    # [], [], ...
                                ],
                                "semantics": {
                                    "surfaces": [],
                                    "values": [],
                                },
                                "texture": {"rgbTexture": {"values": []}},
                            },
                        ],
                        "address": [{"Country": "日本", "Locality": "東京都新宿区西新宿一丁目"}],
                    }
                },
                "vertices": vertices,
                "appearance": {},
                "geometry-templates": {},
            }
            result_debug = json.dumps(result, indent=2, ensure_ascii=False)
            print(result_debug)
            return result


def parse_lod2solid(element_cityObject, vertices_map: VerticesMap):
    # TODO: handling composite surface seriously
    elem_compositeSurface = element_cityObject.find(
        f"./{nsmap['bldg']}lod2Solid/{nsmap['gml']}Solid/{nsmap['gml']}exterior/{nsmap['gml']}CompositeSurface"
    )
    # print(elem_compositeSurface)

    elems_surfaceMember = elem_compositeSurface.iterfind(
        f".//{nsmap['gml']}surfaceMember"
    )

    hrefs = []
    for elem in elems_surfaceMember:
        # print(elem)
        href = elem.get(f"{nsmap['xlink']}href")
        # Remove hash
        href = href[1:]
        # print(href)
        hrefs.append(href)

    elems_member = []

    # Collect linked elements
    for href in hrefs:
        # NOTE: this may not be guaranteed
        elem = element_cityObject.find(f".//*[@{nsmap['gml']}id='{href}']")
        # print(elem)
        elems_member.append(elem)

    exterior_surfaces = []

    for elem in elems_member:
        els_list = elem.iterfind(f".//{nsmap['gml']}posList")
        for el in els_list:
            text = el.text
            chunks = parse_posList(text)
            logger.debug(chunks)
            single_exterior_surface_exterior = []
            for chunk in chunks:
                index = vertices_map.to_index(chunk)
                single_exterior_surface_exterior.append(index)
            single_exterior_surface = [single_exterior_surface_exterior]
            exterior_surfaces.append(single_exterior_surface)

    return exterior_surfaces, vertices_map


def cityjson_from_gml(infiles, precision=16):
    vertices_map = VerticesMap()

    for infile in infiles:
        with open(infile, "r") as f:
            root = etree.parse(f)
            elem_cityObject = root.find(
                f".//{nsmap['bldg']}Building[@{nsmap['gml']}id='BLD_166aaf40-b65b-46c3-b7c7-05f3e7118f46']"
            )

            exterior_surfaces, vertices_map = parse_lod2solid(
                elem_cityObject, vertices_map
            )

            # print("vertices_map.vertices", vertices_map.vertices)

            result = {
                "type": "CityJSON",
                "version": "1.1",
                "extensions": {},
                "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]},
                "metadata": {},
                "CityObjects": {
                    "BLD_f51c1fff-5198-4196-ac9b-39a5c1e48dca": {
                        "type": "Building",
                        # "attributes": {"建物ID": "13104-bldg-52530", "measuredHeight": 61.9},
                        # "children": [
                        #     "ID_22730c8f-9fbc-4d58-88dd-5569d7480fad",
                        #     "ID_598f2fab-030f-429c-b938-a222e04d8e4b",
                        #     "ID_db473977-e95e-4075-b0be-55eb65974610",
                        #     "ID_ac26b2cb-553e-428a-9f10-2659419e824d",
                        # ],
                        "geometry": [
                            # {
                            #     "type": "MultiSurface",
                            #     "lod": "0",
                            #     "boundaries": [],
                            # },
                            {
                                "type": "Solid",
                                "lod": "2",
                                "boundaries": [
                                    # Exterior shell
                                    exterior_surfaces,
                                    # Interior shells
                                    # [], [], ...
                                ],
                                "semantics": {
                                    "surfaces": [],
                                    "values": [],
                                },
                                "texture": {"rgbTexture": {"values": []}},
                            },
                        ],
                        "address": [{"Country": "日本", "Locality": "東京都新宿区西新宿一丁目"}],
                    }
                },
                "vertices": vertices_map.vertices,
                "appearance": {},
                "geometry-templates": {},
            }
            result_debug = json.dumps(result, indent=2, ensure_ascii=False)
            print(result_debug)
            return result
