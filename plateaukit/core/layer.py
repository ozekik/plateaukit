from abc import ABC, abstractmethod

from geopandas import GeoDataFrame


class BaseLayer(ABC):
    """The BaseLayer class."""

    name: str | None

    @abstractmethod
    def get_area(self, bbox: list[float] | None = None) -> "BaseLayer":
        pass


class GeoDataFrameLayer(BaseLayer):
    """The GeoDataFrameLayer class."""

    gdf: GeoDataFrame

    def __init__(self, gdf: GeoDataFrame, *, name: str | None = None) -> None:
        self.gdf = gdf
        self.name = name

    def __repr__(self) -> str:
        return "GeoDataFrameLayer()"

    def get_area(self, bbox: list[float] | None = None):
        area_gdf = (
            self.gdf.cx[bbox[0] : bbox[2], bbox[1] : bbox[3]] if bbox else self.gdf
        )

        # TODO: Error handling when area_gdf is empty

        return GeoDataFrameLayer(area_gdf)
