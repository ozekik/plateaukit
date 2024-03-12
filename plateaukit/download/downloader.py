import os.path
import shutil
from pathlib import Path
from urllib.parse import urlparse

import requests
from rich.progress import wrap_file

API_URL = "https://www.geospatial.jp/ckan/api/3"


def download_resource(resource_id, dest="/tmp"):
    resp = requests.get(f"{API_URL}/action/resource_show", params={"id": resource_id})
    data = resp.json()

    if not data["success"]:
        raise Exception("Failed to download")

    file_url = data["result"]["url"]
    file_name = os.path.basename(urlparse(file_url).path)

    destfile_path = str(Path(dest, file_name))

    # NOTE: If the destfile_path is in the home directory, replace it with ~ for better privacy
    try:
        _destfile_path = Path(destfile_path).relative_to(Path.home())
        _destfile_path = str(Path("~", _destfile_path))
    except:
        _destfile_path = destfile_path

    print(f"Download file as: {_destfile_path}")

    with requests.get(file_url, stream=True) as r:
        value = r.headers.get("Content-Length")
        total_length = int(value) if value is not None else -1
        with wrap_file(r.raw, total=total_length, description="Downloading...") as raw:
            with open(destfile_path, "wb") as output:
                shutil.copyfileobj(raw, output)

    return destfile_path


# download_resource("0bab2b7f-6962-41c8-872f-66ad9b40dcb1")

# NOTE: format
# {
#     "help": "https://www.geospatial.jp/ckan/api/3/action/help_show?name=resource_show",
#     "success": True,
#     "result": {
#         "cache_last_updated": None,
#         "standard_price": "",
#         "package_id": "b7a9b937-2e68-4f33-9c4e-16b5cc7392a8",
#         "datastore_active": False,
#         "id": "0bab2b7f-6962-41c8-872f-66ad9b40dcb1",
#         "size": None,
#         "tos": "",
#         "selection_type": "",
#         "state": "active",
#         "hash": "",
#         "description": "CityGML形式のデータで、次のデータが格納されています。\r\n\r\n* 建築物\r\n* 橋梁\r\n* 道路\r\n* 土地利用・公園\r\n* 地形\r\n* 都市設備\r\n* 洪水浸水想定区域（国管理、都管理）\r\n* 土砂災害警戒区域\r\n* 製品仕様書（PDF形式）\r\n* コードインデックス（XML形式）\r\n* 構築範囲図（PDF形式）\r\n* メタデータ（XML形式）\r\n\r\nファイルサイズは約4.2GBです。\r\n\r\n※2021年9月18日\u3000i-UR1.4は、名前空間及びXMLSchemaファイルの所在が変更されたことに伴い、i-UR1.5に改定されています。\r\n[(https://www.chisou.go.jp/tiiki/toshisaisei/itoshisaisei/iur)](https://www.chisou.go.jp/tiiki/toshisaisei/itoshisaisei/iur)\r\n\r\n各ファイルにおけるこれらの記述は、改定前の記述となっていますのでご注意ください。\r\n\r\n** 更新情報 **\r\n\r\n2022年4月1日\u3000CityGMLのディレクトリを修正しました。\r\n",
#         "format": "ZIP",
#         "last_modified": None,
#         "url_type": None,
#         "metadata_type": "",
#         "mimetype": None,
#         "cache_url": None,
#         "name": "CityGML",
#         "acknowledgement": "",
#         "url": "https://gic-plateau.s3.ap-northeast-1.amazonaws.com/2020/13100_tokyo23-ku_2020_citygml_3_2_op.zip",
#         "created": "2022-04-01T14:31:28.753939",
#         "mimetype_inner": None,
#         "position": 2,
#         "revision_id": "df6da242-128e-42a0-93e4-7b08c607de5d",
#         "data_crs": "",
#         "resource_type": None,
#     },
# }
