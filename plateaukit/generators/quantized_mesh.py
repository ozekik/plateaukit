import numpy as np
from bidict import bidict
from lxml import etree

from plateaukit.constants import default_nsmap
from plateaukit.logger import logger
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


def triangles_from_gml(infiles, precision=8):
    try:
        from quantized_mesh_encoder import encode
    except ImportError:
        logger.error("quantized_mesh_encoder is not installed")
        return

    vertices_map = VerticesMap()

    indices = []

    for infile in infiles:
        with open(infile, "r") as f:
            root = etree.parse(f)
            elems_Triangle = root.iterfind(f".//{default_nsmap['gml']}Triangle")
            for elem_Triangle in elems_Triangle:
                elem_posList = elem_Triangle.find(
                    f"./{default_nsmap['gml']}exterior/{default_nsmap['gml']}LinearRing/{default_nsmap['gml']}posList"
                )
                pos_list = parse_posList(elem_posList.text)
                # Cut off the last element identical to the first
                triangle_vertices = pos_list[:3]
                # print(triangle_vertices)
                triangle_indices = tuple(
                    vertices_map.to_index(v) for v in triangle_vertices
                )
                # print(indices)
                indices.append(triangle_indices)

    vertices = np.array(vertices_map.vertices)
    indices = np.array(indices)
    print(vertices)
    print(indices)

    with open("output.terrain", "wb") as f:
        encode(f, vertices, indices)
