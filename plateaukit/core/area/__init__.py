import tempfile
from typing import Literal, TextIO

import ipydeck
import pydeck

from plateaukit.core.area._export import to_cityjson, to_geojson
from plateaukit.core.area._llm import chat, set_llm
from plateaukit.core.layer import BaseLayer, GeoDataFrameLayer
from plateaukit.core.widgets.cityview_widget import CityViewWidget
from plateaukit.core.widgets.interactive_deck import InteractiveDeck


def _is_colab():
    import sys

    return "google.colab.output" in sys.modules


class Area:
    """This class represents an area of interest."""

    layers: dict[str, BaseLayer]

    def __init__(
        self,
        layer_or_layers: BaseLayer | dict[str, BaseLayer],
        *,
        base_layer_name: str = "bldg",
    ) -> None:
        """Initialize an area of interest.

        Args:
            layer_or_layers: Layer or a dictionary of layers.
            base_layer_name: Name of the base layer. Default is "bldg".
        """
        if isinstance(layer_or_layers, BaseLayer):
            base_layer = layer_or_layers
            layers = {base_layer_name: base_layer}
        elif isinstance(layer_or_layers, dict):
            if base_layer_name is None:
                raise ValueError(
                    "base_layer_name is required when layer_or_layers is a dictionary"
                )
            layers = layer_or_layers
            base_layer = layers[base_layer_name]

        self.layers = layers
        self.base_layer = base_layer
        self.base_layer_name = base_layer_name

        self._datasets: list[str] | None = None

    def __repr__(self) -> str:
        return "Area()"

    @property
    def gdf(self):
        # NOTE: For backward compatibility
        if "bldg" in self.layers and isinstance(self.layers["bldg"], GeoDataFrameLayer):
            return self.layers["bldg"].gdf
        else:
            raise RuntimeError()

    @gdf.setter
    def gdf(self, value):
        # NOTE: For backward compatibility
        if "bldg" in self.layers and isinstance(self.layers["bldg"], GeoDataFrameLayer):
            self.layers["bldg"].gdf = value
        else:
            raise RuntimeError()

    def get_area(self, bbox: list[float] | None = None):
        """Get the specified area from the dataset.

        Args:
            bbox: Bounding box of the area of interest.
                   If not specified, the area of the entire dataset will be returned.
        """

        layers = {name: layer.get_area(bbox) for name, layer in self.layers.items()}

        return Area(layers, base_layer_name=self.base_layer_name)

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
        except Exception:
            pass

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as fp:
            deck.to_html(fp.name, open_browser=True)

    def _show_ipydeck(self):
        deck = InteractiveDeck(self.gdf)

        self.selection = deck.selection

        if _is_colab():
            return deck.deck
        else:
            return deck.widget

    def _show_cityview(self, *, mode: Literal["virtual", "map"] = "virtual", **kwargs):
        widget = CityViewWidget(self, mode=mode, **kwargs)

        # self.selection = deck.selection

        return widget.widget

    def show(
        self,
        renderer: Literal["pydeck", "ipydeck", "cityview"] = "ipydeck",
        # interactive: bool = True,
        embed: bool = True,
        **kwargs,
    ):
        if renderer == "pydeck":
            return self._show_pydeck()
        elif renderer == "ipydeck":
            return self._show_ipydeck()
        elif renderer == "cityview":
            return self._show_cityview(**kwargs)
        else:
            raise ValueError(f"Unknown renderer: {renderer}")

    def dict(self):
        return self.gdf.to_dict()

    def to_geojson(self, file: str | None = None):
        """Export the area in GeoJSON format."""

        return to_geojson(self, file)

    def to_cityjson(
        self,
        file: str | TextIO,
        *,
        types: list[str] | None = None,
        ground: bool = False,
        seq: bool = False,
        target_epsg: int = 4326,
    ):
        """Export the area in CityJSON format."""

        return to_cityjson(
            self, file, types=types, ground=ground, seq=seq, target_epsg=target_epsg
        )

    def set_llm(self, llm):
        return set_llm(self, llm)

    def chat(
        self, message: str, *, output_format: Literal["map", "dataframe"] | None = "map"
    ):
        """LLM-based chat interface for the area of interest using LangChain."""

        return chat(self, message, output_format=output_format)

    @property
    def buildings(self):
        from plateaukit.core.models import Building

        # TODO: Filter and return buildings only

        for row in self.gdf.itertuples():
            df = self.gdf.loc[[row.Index]]

            yield Building(df)
