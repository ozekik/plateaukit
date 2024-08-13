from typing import Literal

from plateaukit.readers.citygml.ir_models import IRDocument
from plateaukit.readers.citygml.reader import Readable

from .geometry import GeometryTransformer


class LODFilteringTransformer(GeometryTransformer):
    def __init__(
        self,
        *,
        mode: Literal["highest", "all", "values"],
        values: list[str] | None = None,
    ):
        self.mode = mode

        if mode == "values" and values is None:
            raise ValueError("Values must be provided in 'values' mode.")

        self.values = values

    def transform(self, readable: Readable):
        readable.transformers.append(self)

        return readable

    def transform_document(self, document: IRDocument):
        if self.mode == "all":
            return document

        for city_object in document.city_objects:
            if self.mode == "highest":
                max_lod_value = max(map(lambda x: x.lod, city_object.geometry))
                city_object.geometry = [
                    geom for geom in city_object.geometry if geom.lod == max_lod_value
                ]
            elif self.mode == "values":
                if self.values is None:
                    raise ValueError("Values must be provided in 'values' mode.")

                city_object.geometry = [
                    geom for geom in city_object.geometry if geom.lod in self.values
                ]
            else:
                raise ValueError(f"Invalid mode: {self.mode}")

        return document
