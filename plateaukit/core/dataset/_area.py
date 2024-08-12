import sys
from typing import Sequence, cast

import flatgeobuf as fgb
import geopandas as gpd

try:
    from pyogrio import read_dataframe
except ImportError:
    read_dataframe = None

from plateaukit import defaults, geocoding
from plateaukit.core.area import Area, GeoDataFrameLayer


def get_area(self):
    """Get the entire area of the dataset."""

    if self.dataset_id.endswith(".cloud"):
        raise Exception("Not supported for cloud datasets")

    dataframes = self.load_gdf()

    layers = {}

    for k, gdf in dataframes.items():
        if self.object_types is None or k in self.object_types:
            layers[k] = GeoDataFrameLayer(gdf)

    if "bldg" not in layers:
        raise RuntimeError("Missing building data")

    area = Area(layers, base_layer_name="bldg")
    area._datasets = [self.dataset_id]

    return area


def area_from_bbox(self, bbox: list[float] | None = None):
    """Get the specified area from the dataset.

    Args:
        bbox: Bounding box of the area of interest.
                If not specified, the area of the entire dataset will be returned.
    """

    if self.dataset_id.endswith(".cloud"):
        if "pyodide" in sys.modules:
            try:
                import pyodide_http  # type: ignore

                pyodide_http.patch_all()
            except Exception:
                pass

        # Load data from remote flatgeobuf
        remote_fgb = defaults.cloud_base_url + self.dataset_id.replace(".cloud", ".fgb")
        if read_dataframe:
            area_gdf = read_dataframe(
                remote_fgb,
                bbox=tuple(bbox) if bbox else None,
            )
            area_gdf = cast(gpd.GeoDataFrame, area_gdf)
        else:
            feature_collection = fgb.load_http(
                remote_fgb,
                bbox=tuple(bbox) if bbox else None,
            )
            area_gdf = gpd.GeoDataFrame.from_features(feature_collection)

        layers = {}
        layers["bldg"] = GeoDataFrameLayer(area_gdf)
        area = Area(layers, base_layer_name="bldg")

    else:
        dataframes = self.load_gdf()

        layers = {}

        for k, gdf in dataframes.items():
            if self.object_types is None or k in self.object_types:
                # TODO: Error handling when area_gdf is empty
                area_gdf = gdf.cx[bbox[0] : bbox[2], bbox[1] : bbox[3]] if bbox else gdf
                layers[k] = GeoDataFrameLayer(area_gdf)

        if "bldg" not in layers:
            raise RuntimeError("`bldg` layer is required")

        area = Area(layers, base_layer_name="bldg")

    area._datasets = [self.dataset_id]

    return area


def area_from_polygons(self, polygons: list[gpd.GeoDataFrame]):
    """Get an area from the dataset by polygons.

    Args:
        polygon: Polygon of the area of interest.
    """

    if self.dataset_id.endswith(".cloud"):
        raise Exception("Not supported for cloud datasets")

    dataframes = self.load_gdf()

    layers = {}

    for k, gdf in dataframes.items():
        if self.object_types is None or k in self.object_types:
            # TODO: Error handling when area_gdf is empty
            area_gdf = gdf[gdf.geometry.intersects(polygons)]
            layers[k] = GeoDataFrameLayer(area_gdf)

    if "bldg" not in layers:
        raise RuntimeError("`bldg` layer is required")

    area = Area(layers, base_layer_name="bldg")

    return area


def area_from_points(
    self, points: list[Sequence[float]], size: list[float] = [1000, 1000]
):
    """Get an area from the dataset by points.

    Args:
        points: List of points of the area of interest.
        size: Size of the area of interest in meters.
    """

    bbox = geocoding._get_bbox(points)
    bbox = geocoding._pad_bbox(bbox, size)

    return self.area_from_bbox(bbox)


def area_from_address(self, address: str, size: list[float] = [1000, 1000]):
    """Get an area from the dataset by an address.

    Args:
        address: Address of the area of interest.
        size: Size of the area of interest in meters.
    """

    bbox = geocoding.bbox_from_address(address, min_size=size)

    return self.area_from_bbox(bbox)


def area_from_postcode(self, postcode: str):
    """Get an area from the dataset by a postcode.

    Args:
        postcode: Postal code of the area of interest.
    """

    bbox = geocoding.bbox_from_postcode(postcode)

    return self.area_from_bbox(bbox)


def area_from_landmark(self, landmark: str, min_size: list[float] = [1000, 1000]):
    """Get an area from the dataset by a landmark.

    Args:
        landmark: Landmark of the area of interest.
    """
    bbox = geocoding.bbox_from_landmark(landmark, min_size=min_size)

    return self.area_from_bbox(bbox)
