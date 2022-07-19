import json
import requests
import zipfile
import os
from typing import OrderedDict, Optional


def save_dict_as_json(data: dict, filename: str) -> None:
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def get_dict_from_json_file(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


def download_zip_file(URL: str, filename: str) -> str:
    data = requests.get(URL)
    with open(filename, "wb") as f:
        f.write(data.content)

    return filename


def unzip_package(zip_filename: str) -> list[Optional[str]]:
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        extracted_file_names = zip_ref.namelist()
        zip_ref.extractall("./")

    return extracted_file_names


def get_files_names_from_dir(dirpath: str) -> list[str]:
    return os.listdir(dirpath)


def save_zip_file(source_filepath: str, output_filepath: str) -> None:
    with zipfile.ZipFile(output_filepath, "w") as zip:
        zip.write(source_filepath)