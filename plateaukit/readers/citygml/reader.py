import io
import math
import os.path
import re
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile, is_zipfile

from fs import open_fs

from plateaukit import utils
from plateaukit.readers.citygml import PLATEAUCityGMLParser

# from plateaukit.utils import dict_key_to_camel_case
from .ir_models import IRDocument, IRMetadata


class Readable:
    def __init__(self, files, *args, reader_cls, transformers=[], **kwargs):
        self.reader_cls = reader_cls
        self.reader = reader_cls()
        self.files = files
        self.transformers = transformers
        self.args = args
        self.kwargs = kwargs

    def read(self):
        # TODO: Refactoring
        document = self.reader.read_files(self.files, *self.args, **self.kwargs)

        for transformer in self.transformers:
            document = transformer.transform_document(document)

        return document

    def split(self, split_n):
        group_size = math.ceil(len(self.files) / split_n)

        return [
            Readable(
                files,
                *self.args,
                reader_cls=self.reader_cls,
                **self.kwargs,
            )
            for files in utils.chunker(self.files, group_size)
        ]

    def __len__(self):
        return len(self.files)


@dataclass
class ConcurrentStatus:
    quit = None


# TODO: Derive PLATEAUCityGMLReader or ZippedCityGMLReader
class CityGMLReader:
    def __init__(self, concurrent_status=ConcurrentStatus()):
        self.concurrent_status = concurrent_status

    def _make_codelist_file_map(self, codelist_infiles, base_path, *, zip_fs=None):
        _open = zip_fs.open if zip_fs else open

        codelist_file_map = dict()

        for codelist_infile in codelist_infiles:
            with _open(codelist_infile, "rb") as f:
                relative_path = os.path.relpath(codelist_infile, base_path)
                codelist_file_map[relative_path] = io.BytesIO(f.read())

        return codelist_file_map

    def scan_files(
        self,
        infiles,
        *,
        # object_types,
        # lod,
        codelist_infiles=None,
        zipfile=None,
        selection: list[str] | None = None,
    ):
        """Return a Readable object for the given files."""

        if not codelist_infiles:
            # Codelists
            codelist_infiles = []
            pat = re.compile(r".*codelists\/.*\.xml$")

            if zipfile and is_zipfile(zipfile):
                with ZipFile(zipfile) as f:
                    namelist = f.namelist()
                    codelist_infiles = list(filter(lambda x: pat.match(x), namelist))
                    # NOTE: zipfs requires POSIX path
                    codelist_infiles = [
                        str(Path("/", target)) for target in codelist_infiles
                    ]
            else:
                # TODO: Test support for non-zip codelists
                raise NotImplementedError()
                # codelist_infiles += [str(Path(file_path, "codelists", "*.xml"))]

        return Readable(
            infiles,
            reader_cls=CityGMLReader,
            codelist_infiles=codelist_infiles,
            zipfile=zipfile,
            selection=selection,
        )

    def read_files(
        self,
        infiles,
        *,
        # object_types,
        # lod,
        codelist_infiles=None,
        zipfile=None,
        target_epsg=3857,  # TODO: Fix this
        selection: list[str] | None = None,
    ):
        if zipfile is not None:
            zip_fs = open_fs(f"zip://{zipfile}")
        else:
            zip_fs = None

        if not codelist_infiles:
            # Codelists
            codelist_infiles = []
            pat = re.compile(r".*codelists\/.*\.xml$")

            if zipfile and is_zipfile(zipfile):
                with ZipFile(zipfile) as f:
                    namelist = f.namelist()
                    codelist_infiles = list(filter(lambda x: pat.match(x), namelist))
                    # NOTE: zipfs requires POSIX path
                    codelist_infiles = [
                        str(Path("/", target)) for target in codelist_infiles
                    ]
            else:
                # TODO: Test support for non-zip codelists
                raise NotImplementedError()
                # codelist_infiles += [str(Path(file_path, "codelists", "*.xml"))]

        # Load codelists
        codelist_file_map = {}
        if infiles:
            base_path = Path(infiles[0]).parent  # TODO: Fix this
            codelist_file_map = self._make_codelist_file_map(
                codelist_infiles, base_path, zip_fs=zip_fs
            )

        parser = PLATEAUCityGMLParser(
            target_epsg=target_epsg, codelist_file_map=codelist_file_map
        )

        _open = zip_fs.open if zip_fs else open

        city_objects = []
        for i, infile in enumerate(infiles):
            with _open(infile, "rb") as f:
                co_iter = parser.iterparse(f, selection=selection)

                for city_obj in co_iter:
                    # if object_types is not None and city_obj.type not in object_types:
                    #     continue
                    if (
                        self.concurrent_status.quit
                        and self.concurrent_status.quit.is_set()
                    ):
                        exit()

                    city_objects.append(city_obj)

        if zip_fs:
            zip_fs.close()

        return IRDocument(
            metadata=IRMetadata(epsg=target_epsg),  # TODO: Fix
            city_objects=city_objects,
        )
