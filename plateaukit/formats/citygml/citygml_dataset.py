import io
import re
import zipfile
from pathlib import Path

from fs import open_fs
from lxml import etree

from plateaukit import parsers
from plateaukit.config import Config
from plateaukit.logger import logger
from plateaukit.parsers import constants


class CityGMLDataset:
    """A parser for PLATEAU CityGML datasets.

    Attributes:
        dataset_id: Dataset ID.
    """

    dataset_id: str

    def __init__(self, dataset_id: str):
        """Initialize a dataset.

        Args:
            dataset_id: Dataset ID
        """
        # TODO: Support zip file as input

        self.dataset_id = dataset_id

        config = Config()
        record = config.datasets.get(self.dataset_id, None)

        if not record:
            raise RuntimeError("Missing dataset record")

        if "citygml" not in record:
            raise RuntimeError("Missing CityGML data")

        file_path = Path(record["citygml"])

        self.file_path = file_path

    def udx_dirs(self):
        """List UDX directories in the dataset."""

        pat = re.compile(rf".*udx\/([^\/]*?)\/$")

        with zipfile.ZipFile(self.file_path) as f:
            namelist = f.namelist()
            dirs = {
                pat.match(target).group(1): str(Path("/", pat.match(target).group(0)))
                for target in namelist
                if pat.match(target)
            }

        return dirs

    def _list_udx_files(self, udx_type: str):
        """List files of a udx type in the dataset."""

        udx_dirs = self.udx_dirs()

        if udx_type not in udx_dirs:
            raise RuntimeError(f"Missing udx directory: {udx_type}")

        pat = re.compile(rf".*\/udx\/{udx_type}\/[^\/]*\.gml$")
        with zipfile.ZipFile(self.file_path) as f:
            namelist = f.namelist()
            files = list(filter(lambda x: pat.match(x), namelist))
            files = [str(Path("/", target)) for target in files]

        return files

    def scan_attributes(self, udx_type: str):
        """Scan city object properties in the dataset."""

        files = self._list_udx_files(udx_type)

        codelists = self.codelists()

        zip_fs = open_fs(f"zip://{self.file_path}")

        props = []

        for file in files:
            base_path = Path(file).parent

            with zip_fs.open(file, "rb") as f:
                root = etree.parse(f).getroot()
                for city_obj in root.iterfind(
                    ".//core:cityObjectMember/*", constants.nsmap
                ):
                    for el in city_obj:
                        _qname = etree.QName(el)
                        ns = _qname.namespace
                        localname = _qname.localname
                        ns_prefix = constants.nsmap.inverse.get(ns, None)
                        if ns_prefix:
                            qname = f"{ns_prefix}:{localname}"
                        else:
                            qname = _qname.text

                        prop = {
                            "tag": qname,
                        }

                        if el.tag == f"{{{constants.nsmap['gen']}}}stringAttribute":
                            name = el.attrib["name"]
                            prop["name"] = name

                        if (
                            el.tag
                            == f"{{{constants.nsmap['uro']}}}keyValuePairAttribute"
                        ):
                            for child in el.iterfind(
                                "./uro:KeyValuePairAttribute", constants.nsmap
                            ):
                                # print("child", child)
                                el_key = child.find("./uro:key", constants.nsmap)
                                key = el_key.text
                                codelist_path = el_key.attrib.get("codeSpace", None)
                                codelist_path = str(
                                    Path(base_path, codelist_path).resolve()
                                )
                                # print("codelist_path", codelist_path)
                                codelist = codelists.get(codelist_path, None)
                                # print("codelist", codelist)
                                if codelist:
                                    key_name = codelist[key]
                                    prop["name"] = key_name

                        if not "name" in prop:
                            if qname in constants.tag_display_names:
                                prop["name"] = constants.tag_display_names[qname].get(
                                    "ja", None
                                )
                            else:
                                prop["name"] = localname

                        if prop not in props:
                            props.append(prop)
                            yield prop
                            # logger.debug(f"{prop}")

    def codelists(self):
        """Get codelists from the dataset."""

        file_path = self.file_path

        codelist_infiles = []

        pat = re.compile(rf".*codelists\/.*\.xml$")

        with zipfile.ZipFile(file_path) as f:
            namelist = f.namelist()
            codelist_infiles = list(filter(lambda x: pat.match(x), namelist))
            codelist_infiles = [str(Path("/", target)) for target in codelist_infiles]

        zip_fs = open_fs(f"zip://{file_path}")

        codelist_file_map = dict()

        for codelist_infile in codelist_infiles:
            if zipfile is not None:
                with zip_fs.open(codelist_infile, "rb") as f:
                    codelist_file_map[codelist_infile] = io.BytesIO(f.read())
            else:
                with open(codelist_infile, "rb") as f:
                    codelist_file_map[codelist_infile] = io.BytesIO(f.read())

        codelists = {}

        for codelist_infile, file_obj in codelist_file_map.items():
            parser = parsers.CodelistParser()
            codelists[codelist_infile] = parser.parse(file_obj)

        return codelists