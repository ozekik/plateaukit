import io
import re
import zipfile
from os import PathLike
from pathlib import Path

from bidict import bidict
from fs import open_fs
from lxml import etree

from plateaukit.config import Config
from plateaukit.formats.citygml import constants
from plateaukit.formats.citygml.parsers import CodelistParser


class CityGMLDataset:
    """A (PLATEAU) CityGML dataset.

    Attributes:
        dataset_id: Dataset ID.
    """

    dataset_id: str

    def __init__(self, dataset_id: str | PathLike):
        """Initialize a dataset.

        Args:
            dataset_id: Dataset ID
        """
        # TODO: Support zip file as input

        self.dataset_id = str(dataset_id)

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

        pat = re.compile(r".*udx\/([^\/]*?)\/$")

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

        pat = re.compile(rf".*udx\/{udx_type}\/[^\/]*\.gml$")
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
                # Get namespace map
                itertree = etree.iterparse(f, events=("end",))
                _, root = next(itertree)
                f.seek(0)
                infile_nsmap = bidict(root.nsmap)

                tag = f"{{{infile_nsmap['core']}}}cityObjectMember"
                itertree = etree.iterparse(f, events=("end",), tag=tag)
                _, root = next(itertree)

                for _ev, co_root in itertree:
                    it = co_root.iterchildren()
                    city_obj = next(it)

                    for el in city_obj:
                        _qname = etree.QName(el)
                        ns = _qname.namespace
                        localname = _qname.localname
                        ns_prefix = infile_nsmap.inverse.get(ns, None)
                        if ns_prefix:
                            qname = f"{ns_prefix}:{localname}"
                        else:
                            qname = _qname.text

                        prop = {
                            "tag": qname,
                        }

                        if (
                            "gen" in infile_nsmap
                            and el.tag == f"{{{infile_nsmap['gen']}}}stringAttribute"
                        ):
                            name = el.attrib["name"]
                            prop["name"] = name

                        elif (
                            "uro" in infile_nsmap
                            and el.tag
                            == f"{{{infile_nsmap['uro']}}}keyValuePairAttribute"
                        ):
                            for child in el.iterfind(
                                "./uro:KeyValuePairAttribute", infile_nsmap
                            ):
                                # print("child", child)
                                el_key = child.find("./uro:key", infile_nsmap)
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

                        if "name" not in prop:
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

                    # co_root.clear()  # NOTE: Bad performance impact
                    root.clear()  # NOTE: Unnecessary?

    def codelists(self):
        """Get codelists from the dataset."""

        file_path = self.file_path

        codelist_infiles = []

        pat = re.compile(r".*codelists\/.*\.xml$")

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
            parser = CodelistParser()
            codelists[codelist_infile] = parser.parse(file_obj)

        return codelists
