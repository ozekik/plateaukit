from textwrap import dedent
from typing import Literal

from plateaukit.core.widgets.interactive_deck import InteractiveDeck


def _is_colab():
    import sys

    return "google.colab.output" in sys.modules


def set_llm(self, llm):
    self.llm = llm


def chat(
    self, message: str, *, output_format: Literal["map", "dataframe"] | None = "map"
):
    """LLM-based chat interface for the area of interest using LangChain."""

    import geopandas as gpd

    try:
        from langchain_core.output_parsers.openai_tools import (
            JsonOutputKeyToolsParser,
        )
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_experimental.tools import PythonAstREPLTool
    except ImportError:
        raise ImportError(
            "Please install langchain-core and langchain-experimental to use this feature."
        )

    if not hasattr(self, "llm") or self.llm is None:
        raise RuntimeError("Set LangChain's LLM instance with set_llm() method first.")

    llm = self.llm

    df = self.gdf.copy()

    tool = PythonAstREPLTool(globals={"df": df}, verbose=True)
    tool.locals = tool.globals
    llm_with_tools = llm.bind_tools([tool], tool_choice=tool.name)
    parser = JsonOutputKeyToolsParser(key_name=tool.name, first_tool_only=True)

    system = dedent(
        f"""You have access to a geopandas dataframe called `df`.
        Please output Python code in response to the user's instructions. Do not output anything else.
        The following is the result of executing `df.head().to_markdown()`:
        {df.head().to_markdown()}
        The following is a description of the items in this dataframe:
        - buildingId: The ID of the building
        - name: The name of the building. Always look for the name of the building in this field
        - measuredHeight: The measured height of the building
        - storeysAboveGround: The number of floors above ground
        - storeysBelowGround: The number of floors below ground
        - usage: The usage of the building
        - longitude: The latitude of the building
        - latitude: The longitude of the building
        The following is a list of buildings whose names exist in this dataframe:
        {df['name'].unique()}
        The following is a list of the usage types of buildings that exist in this data frame:
        {df['usage'].unique()}
        Again, please output Python code in response to the user's instructions. Do not output anything else.
        Do not use any knowledge about the coordinates other than the dataframe.
        Only the standard Python libraries, pandas, and geopandas can be used as libraries.
        Be sure to write Python code that returns a pandas dataframe."""
    )

    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", "{input}")]
    )

    chain = prompt | llm_with_tools | parser | tool

    response = chain.invoke(message)

    if isinstance(response, gpd.GeoDataFrame) and output_format == "map":
        deck = InteractiveDeck(response)

        self.selection = deck.selection

        if _is_colab():
            return deck.deck
        else:
            return deck.widget

    return response
