# %%
from time import sleep
from urllib.parse import urlparse

import requests
from rich.progress import wrap_file

from plateaukit.download.list import city_list

API_URL = "https://www.geospatial.jp/ckan/api/3"

# print(city_list)


def sizeof_fmt(num, suffix="B"):
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Y{suffix}"


def head_resource_size(resource_id, dest="/tmp"):
    resp = requests.get(f"{API_URL}/action/resource_show", params={"id": resource_id})
    data = resp.json()

    if not data["success"]:
        raise Exception("Failed to download")

    file_url = data["result"]["url"]

    with requests.head(file_url) as r:
        size = r.headers.get("Content-Length", None)
        size = int(size) if size is not None else None
        return size
        # print(r.headers)
        # # Get content size as human readable bytes or megabytes or gigabytes
        # content_length = int(r.headers.get("Content-Length"))
        # print(content_length)

    #     total_length = int(r.headers.get("Content-Length"))
    #     with wrap_file(r.raw, total_length, description="Downloading...") as raw:
    #         with open(destfile_path, "wb") as output:
    #             shutil.copyfileobj(raw, output)

    # return destfile_path

def main():
    res = []

    for city in city_list:
        if not city.get("latest", None):
            continue

        # print(city["dataset_id"], city["citygml"])

        size = head_resource_size(city["citygml"])

        print((city["dataset_id"], sizeof_fmt(size)))

        res.append((size, city["dataset_id"], sizeof_fmt(size)))

        sleep(0.5)

    res = sorted(res, key=lambda x: x[0])

    print("\nSorted by size:")

    for r in res:
        print(r[2], r[1])

if __name__ == "__main__":
    main()
