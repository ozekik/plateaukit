import warnings

from lxml import etree


# TODO: Inherit etree.Element?
# NOTE: This class MUST be lightweight
class CityObjectXML:
    """A CityGML object XML with utility methods.

    Attributes:
        codelist_map: A map from codelist path to corresponding dict.
    """

    nsmap: dict[str, str]
    codelist_map: dict[str, dict[str, str]]  # TODO: Class or instance variable?

    def __init__(
        self,
        el: etree._Element,
        *,
        nsmap: dict[str, str],
        codelist_map: dict[str, dict[str, str]] = {},
    ):
        self.tree = el
        self.nsmap = nsmap
        self.codelist_map = codelist_map

    def _get_codespace_attribute(self, xpath) -> str | None:
        el = self.tree.find(xpath, self.nsmap)

        if el is None:
            return None

        # Check if el has codeSpace attribute
        if (code_space_path := el.get("codeSpace")) is not None:
            code_dict = self.codelist_map.get(code_space_path, None)
            key = el.text

            if code_dict is None or key is None:
                return None

            value = code_dict.get(key, None)
            return value

        value = el.text if el is not None else None
        return value

    def get_gml_id(self) -> str | None:
        """Get gml:id of a CityGML object."""

        path = "./[@gml:id]"
        result = self.tree.find(path, self.nsmap)

        if result is None:
            warnings.warn(
                "gml:id not found"
                # f"gml:id not found\n{etree.tostring(tree, pretty_print=True).decode()}"
            )
            return None

        id = result.get(f"{{{self.nsmap['gml']}}}id")

        return id if id is not None else None

    def find(self, *args, **kwargs):
        return self.tree.find(*args, **kwargs)
