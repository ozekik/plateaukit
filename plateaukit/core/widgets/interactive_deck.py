import json
from io import StringIO

import geopandas as gpd
import ipydeck
import ipywidgets as widgets
import pandas as pd
import pydeck
from IPython.display import display

import plateaukit.core as core


class InteraciveDeck:
    def __init__(self, gdf: gpd.GeoDataFrame, opacity=1) -> None:
        self.gdf = gdf
        self.deck = self._init_deck(opacity=opacity)

        # Set selection area
        empty_gdf = gpd.GeoDataFrame()
        self.selection = core.area.Area(empty_gdf)

        self._widget_df = self.gdf.copy()

        self.out = widgets.Output()

        def display_df():
            with self.out:
                display(self._widget_df, clear=True)

            return self.out

        self.deck.observe(self.click_handler, names="click")

        self.widget = widgets.VBox([self.deck, self.out])

    def _init_deck(self, opacity=1):
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

        building_layer = self._create_building_layer(self.gdf, opacity=opacity)

        deck = ipydeck.Deck(
            layers=[building_layer],
            initial_view_state=view_state,
            tooltip={
                "html": "${name ? name : buildingId}",
                "style": {
                    "font-family": "sans-serif",
                    "font-size": "8px",
                    "color": "white",
                },
            },
        )

        return deck

    def _create_building_layer(self, df, opacity=1):
        layer = ipydeck.Layer(
            "GeoJsonLayer",
            data=df,
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
            on_click=True,
        )
        return layer

    def click_handler(self, change):
        feature = change["new"]
        # print("clicked", feature)

        if "fill_color" in feature["properties"]:
            del feature["properties"]["fill_color"]

        # NOTE: https://github.com/heremaps/xyz-spaces-python/pull/115
        buf = json.dumps(feature)
        row = gpd.read_file(StringIO(buf))

        if self.selection.gdf.empty:
            self.selection.gdf = row
        else:
            # If self.selection.gdf contains the row, remove it
            if row.at[0, "buildingId"] in self.selection.gdf["buildingId"].values:
                self.selection.gdf = self.selection.gdf[
                    ~self.selection.gdf.loc[:, "buildingId"].isin(row["buildingId"])
                ]
            else:
                self.selection.gdf = pd.concat([self.selection.gdf, row])

        overlap_df = self._widget_df.loc[
            self._widget_df.loc[:, "buildingId"].isin(self.selection.gdf["buildingId"])
        ]

        # Add fill_color column to df if it doesn't exist
        if "fill_color" not in self._widget_df.columns:
            self._widget_df.loc[:, "fill_color"] = None

        self._widget_df["fill_color"] = self._widget_df.loc[
            self._widget_df.index.isin(overlap_df.index), "fill_color"
        ].apply(lambda x: [255, 0, 0])

        updated_layer = self._create_building_layer(self._widget_df)
        self.deck.layers = [updated_layer]

        self.deck.update()

        # Delete fill_color column
        self._widget_df.drop(columns=["fill_color"], inplace=True)

        with self.out:
            # print("clicked", feature)
            display(
                self._widget_df.iloc[self._widget_df.index.isin(overlap_df.index)],
                clear=True,
            )
