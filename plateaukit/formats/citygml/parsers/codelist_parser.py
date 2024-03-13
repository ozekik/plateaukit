from lxml import etree

from plateaukit.formats.citygml.constants import nsmap


class CodelistParser:
    """A parser for codelists."""

    def __init__(self):
        pass

    def parse(self, infile):
        tree = etree.parse(infile)
        root = tree.getroot()

        result = dict()

        for el in root.iterfind(".//gml:dictionaryEntry/gml:Definition", nsmap):
            # print(el)

            el_key = el.find("./gml:name", nsmap)
            key = el_key.text if el_key is not None else None

            el_value = el.find("./gml:description", nsmap)
            value = el_value.text if el_value is not None else None

            if key is not None:
                result[key] = value

        return result
