import tempfile

from geopandas import GeoDataFrame


class Building:
    """This class represents a building."""

    gdf: GeoDataFrame

    def __init__(self, gdf: GeoDataFrame) -> None:
        """Initialize a building.

        Args:
            gdf: GeoDataFrame representing the building.
        """
        self.gdf = gdf

    def show(self):
        import pydeck

        # bbox = self.gdf.total_bounds
        bbox = self.gdf.buffer(0.001).total_bounds
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
                    get_fill_color=[255, 255, 255],
                    extruded=True,
                    get_elevation="measuredHeight",
                    pickable=True,
                )
            ],
            initial_view_state=view_state,
            tooltip={
                "html": "<b>ID:</b> {id}",
                "style": {
                    "font-family": "sans-serif",
                    "font-size": "8px",
                    "color": "white",
                },
            },
        )

        try:
            if __IPYTHON__:  # type: ignore
                return deck.to_html()
        except:
            pass

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as fp:
            deck.to_html(fp.name, open_browser=True)

    def geojson(self):
        raise NotImplementedError()

    def cityjson(self):
        raise NotImplementedError()

    @property
    def attributes(self):
        """Return the attributes of the building."""

        # TODO:
        # - lng, lat

        return {
            "id": self.gdf.id.iloc[0],
            "measuredHeight": self.gdf.measuredHeight.iloc[0],
            # "roofType": self.gdf.roofType.iloc[0],
            # "roofShape": self.gdf.roofShape.iloc[0],
            # "roofMaterial": self.gdf.roofMaterial.iloc[0],
            # "roofColor": self.gdf.roofColor.iloc[0],
            # "facadeMaterial": self.gdf.facadeMaterial.iloc[0],
            # "facadeColor": self.gdf.facadeColor.iloc[0],
            # "buildingType": self.gdf.buildingType.iloc[0],
        }

    def __repr__(self):
        return f"Building(id={self.gdf.id.iloc[0]})"
