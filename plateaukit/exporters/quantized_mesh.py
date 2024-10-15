# %%
import fast_simplification
import numpy as np
from bidict import bidict
from lxml import etree
from pyproj import Transformer

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
        from quantized_mesh_encoder.encode import encode
    except ImportError:
        logger.error("quantized_mesh_encoder is not installed")
        return

    vertices_map = VerticesMap()

    faces = []

    for infile in infiles:
        with open(infile, "r") as f:
            root = etree.parse(f)
            elems_Triangle = root.iterfind(f".//{{{default_nsmap['gml']}}}Triangle")
            for elem_Triangle in elems_Triangle:
                elem_posList = elem_Triangle.find(
                    f"./{{{default_nsmap['gml']}}}exterior/{{{default_nsmap['gml']}}}LinearRing/{{{default_nsmap['gml']}}}posList"
                )
                pos_list = parse_posList(elem_posList.text)
                # Cut off the last element identical to the first
                triangle_vertices = pos_list[:3]
                # print(triangle_vertices)
                triangle_indices = tuple(
                    vertices_map.to_index(v) for v in triangle_vertices
                )
                # print(indices)
                faces.append(triangle_indices)

    vertices = np.array(vertices_map.vertices)
    faces = np.array(faces)

    # Japan to Web Mercator
    transformer = Transformer.from_crs("EPSG:4612", "EPSG:3857")
    vertices = np.array([transformer.transform(*v) for v in vertices], dtype=np.float32)
    # Transform xy only, keep z
    # vertices = np.array(
    #     [(*transformer.transform(*v[:2]), v[2]) for v in vertices],
    #     dtype=np.float32,
    # )
    # faces
    print(vertices)
    print(faces)
    print(len(vertices), len(faces))
    vertices_out, faces_out = fast_simplification.simplify(
        vertices, faces, 0.9, verbose=True
    )
    print(len(vertices_out), len(faces_out))

    with open("/tmp/output.terrain", "wb") as f:
        encode(f, vertices_out, faces_out)


def main():
    import glob

    infiles = glob.glob("/tmp/hakone-dem/*.gml")
    print(infiles)
    triangles_from_gml(infiles)


if __name__ == "__main__":
    main()
