import tempfile
from typing import Literal

import ipydeck
import pydeck
from geopandas import GeoDataFrame

from plateaukit.core.widgets.interactive_deck import InteraciveDeck
from plateaukit.logger import logger


def _is_colab():
    import sys

    return "google.colab.output" in sys.modules


class Area:
    """This class represents an area of interest."""

    def __init__(self, gdf: GeoDataFrame) -> None:
        """Initialize an area from a GeoDataFrame.

        Args:
            gdf: GeoDataFrame of the area of interest.
        """
        self.gdf = gdf
        self._datasets: list[str] | None = None

    def __repr__(self) -> str:
        return f"Area()"

    def get_area(self, bbox: list[float] | None = None):
        """Get the specified area from the dataset.

        Args:
            bbox: Bounding box of the area of interest.
                   If not specified, the area of the entire dataset will be returned.
        """

        area_gdf = (
            self.gdf.cx[bbox[0] : bbox[2], bbox[1] : bbox[3]] if bbox else self.gdf
        )

        # TODO: Error handling when area_gdf is empty

        return Area(area_gdf)

    def get_centroid(self) -> list[float]:
        """Get the centroid of the area of interest."""

        bbox = self.gdf.total_bounds
        return [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]

    def pydeck(self, opacity: float = 1):
        # cx, cy = self.get_centroid()

        bbox = self.gdf.total_bounds
        points = [(bbox[0], bbox[1]), (bbox[2], bbox[3])]
        # print(points)

        view_state = pydeck.data_utils.compute_view(points, view_proportion=1)
        view_state.pitch = 45

        deck = pydeck.Deck(
            layers=[
                pydeck.Layer(
                    "GeoJsonLayer",
                    data=self.gdf,
                    filled=True,
                    get_fill_color="fill_color || color || [255, 255, 255]",
                    # get_fill_color=[255, 255, 255, 240],
                    # get_line_color=[255, 255, 255],
                    opacity=opacity,
                    extruded=True,
                    # wireframe=True,
                    get_elevation="measuredHeight",
                    pickable=True,
                    auto_highlight=True,
                )
                # pydeck.Layer(
                #     "PolygonLayer",
                #     data=self.gdf,
                #     get_polygon="geometry.coordinates",
                #     filled=True,
                #     stroked=False,
                #     get_fill_color=[0, 0, 0, 20],
                #     get_line_color=[0, 0, 0, 20],
                # )
            ],
            initial_view_state=view_state,
            # initial_view_state=pydeck.ViewState(
            #     latitude=cy,
            #     longitude=cx,
            #     zoom=1,
            #     pitch=0,
            #     bearing=0,
            # ),
            tooltip={
                "style": {
                    "font-family": "sans-serif",
                    "font-size": "8px",
                    "color": "white",
                },
            },
        )

        return deck

    def ipydeck(self, opacity: float = 1):
        bbox = self.gdf.total_bounds
        points = [(bbox[0], bbox[1]), (bbox[2], bbox[3])]
        # print(points)

        view_state = pydeck.data_utils.compute_view(points, view_proportion=1)
        # print(view_state, type(view_state))
        view_state.pitch = 45

        view_state = ipydeck.ViewState(
            **{
                "longitude": view_state.longitude,
                "latitude": view_state.latitude,
                "zoom": view_state.zoom,
                "min_zoom": view_state.min_zoom,
                "max_zoom": view_state.max_zoom,
                "pitch": view_state.pitch,
                "bearing": view_state.bearing,
            }
        )

        deck = ipydeck.Deck(
            layers=[
                ipydeck.Layer(
                    "GeoJsonLayer",
                    data=self.gdf,
                    filled=True,
                    get_fill_color="@@=(properties.fill_color || properties.color || [255, 255, 255])",
                    # get_fill_color=[255, 255, 255, 240],
                    # get_line_color=[255, 255, 255],
                    opacity=opacity,
                    extruded=True,
                    # wireframe=True,
                    get_elevation="@@=properties.measuredHeight",
                    pickable=True,
                    auto_highlight=True,
                )
            ],
            initial_view_state=view_state,
            # tooltip={
            #     "style": {
            #         "font-family": "sans-serif",
            #         "font-size": "8px",
            #         "color": "white",
            #     },
            # },
        )

        return deck

    def _show_pydeck(self):
        deck = self.pydeck()

        deck._tooltip = {
            "html": "<b>ID:</b> {buildingId}",
            "style": {
                "font-family": "sans-serif",
                "font-size": "8px",
                "color": "white",
            },
        }

        try:
            if __IPYTHON__:  # type: ignore
                return deck.to_html()
        except:
            pass

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as fp:
            deck.to_html(fp.name, open_browser=True)

    def _show_ipydeck(self):
        deck = InteraciveDeck(self.gdf)

        self.selection = deck.selection

        if _is_colab():
            return deck.deck
        else:
            return deck.widget

    def show(
        self,
        renderer: Literal["pydeck", "ipydeck"] = "ipydeck",
        # interactive: bool = True,
        embed: bool = True,
    ):
        if renderer == "pydeck":
            return self._show_pydeck()
        elif renderer == "ipydeck":
            return self._show_ipydeck()
        else:
            raise ValueError(f"Unknown renderer: {renderer}")

    def dict(self):
        return self.gdf.to_dict()

    def to_geojson(self):
        """Convert the area to GeoJSON."""

        data = self.gdf.to_json()

        return data

    def to_cityjson(
        self,
        file: str,
        type: list[str] = ["bldg"],
        ground: bool = False,
        target_epsg: int | None = None,
    ):
        """Convert the area to CityJSON."""

        # TODO: Support IOBase as file

        from plateaukit import Dataset

        if self._datasets is None:
            raise RuntimeError("Missing dataset information")

        selection = self.gdf["buildingId"].tolist()

        logger.debug(selection)

        for dataset_id in self._datasets:
            dataset = Dataset(dataset_id)
            dataset.to_cityjson(
                file, ground=ground, selection=selection, target_epsg=target_epsg
            )

    @property
    def buildings(self):
        from plateaukit.core.models import Building

        # TODO: Filter and return buildings only

        for row in self.gdf.itertuples():
            df = self.gdf.loc[[row.Index]]

            yield Building(df)
