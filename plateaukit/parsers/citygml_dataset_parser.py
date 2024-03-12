from os import PathLike

from plateaukit.formats.citygml import CityGMLDataset


class CityGMLDatasetParser:
    def __init__(self):
        pass

    def load_dataset(self, infile: str | PathLike):
        return CityGMLDataset(infile)
