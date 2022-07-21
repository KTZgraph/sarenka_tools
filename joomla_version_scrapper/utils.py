import json
import requests
import zipfile
import os
from typing import Optional


def save_dict_as_json(data: dict, filename: str) -> None:
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def get_dict_from_json_file(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


def download_zip_file(URL: str, dst_filepath: str) -> str:
    data = requests.get(URL)
    with open(dst_filepath, "wb") as f:
        f.write(data.content)

    return dst_filepath


def unzip_package(zip_filename: str, extract_destination="./") -> list[Optional[str]]:
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        extracted_file_names = zip_ref.namelist()
        zip_ref.extractall(extract_destination)

    return extracted_file_names


def get_files_names_from_dir(dirpath: str) -> list[str]:
    return os.listdir(dirpath)


def save_zip_file(source_filepath: str, output_filepath: str) -> None:
    with zipfile.ZipFile(output_filepath, "w") as zip:
        zip.write(source_filepath)


def create_dir_if_not_exists(dir_path: str):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def get_folder_structure(filepath: str) -> list[str]:
    """zwraca po kolei foldery do pliku 
    - całą struktura katalogów potrzerbna do stworzenia drzewka folderów"""
    folders_list = filepath.split("/")
    structure = []
    for deph in range(len(folders_list)):
        tmp_path = [folders_list[i] for i in range(deph)]
        tmp_path = ("/").join(tmp_path)
        if tmp_path != "":
            structure.append(tmp_path)

    return structure


def create_folder_structure(structure: list[str]) -> None:
    """Tworzy strukturę folderów na podstawie listy plików """
    for dirpath in structure:
        create_dir_if_not_exists(dirpath)
