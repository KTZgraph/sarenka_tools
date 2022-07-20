import utils
import os
import shutil


class PackageSaver:
    def __init__(self, filepath: str, output_dir: str = "output_joomla") -> None:
        self.data = utils.get_dict_from_json_file(filepath)
        self.output_dir = output_dir
        self.platform_files_dir = "joomla_platform"
        # ściezka na pobrane zipy
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        # scieżka na striukturę plików platform.php
        if not os.path.isdir(self.platform_files_dir):
            os.mkdir(self.platform_files_dir)

    def parse_info(self, version_info: dict[str, str]) -> dict[str, str]:
        for version_number, url in version_info.items():
            zip_filename = url.split("/")[-1].split("?")[0]
            joomla_dir_name = zip_filename.split(".")[0]

            return version_number, url, zip_filename, joomla_dir_name

    def get_platform_file(self, extracted_files_info: list[str]):
        # w plikach platform.php są informację o wersjach
        platform_files = []
        for filepath in extracted_files_info:
            if "platform.php" in filepath:
                platform_files.append(filepath)
        return platform_files

    def get_folder_structure(self, dst_filepath: str):
        folders_list = dst_filepath.split("/")
        f_length = len(folders_list)
        structure = []
        for deph in range(f_length):
            # WARNING zagnieżdzenia straszne
            tmp_path = [folders_list[i] for i in range(deph)]
            tmp_path = ("/").join(tmp_path)
            if tmp_path != "":
                structure.append(tmp_path)

        return structure

    def create_folder_structure(self, dst_filepath: str):
        structure = self.get_folder_structure(dst_filepath)
        for path_s in structure:
            if not os.path.isdir(path_s):
                os.mkdir(path_s)

    def copy_platform_files(
        self,
        joomla_dir_name: str,
        platform_files: list[str],
        src_dir: str,
    ) -> list[str]:
        for platform_filepath in platform_files:
            # TODO - kopiowanie plików
            src_filepath = f"{src_dir}/{platform_filepath}"
            # print("src_filepath:", src_filepath)
            dst_filepath = (
                f"{self.platform_files_dir}/{joomla_dir_name}/{platform_filepath}"
            )
            # print("dst_filepath:", dst_filepath)

            self.create_folder_structure(dst_filepath)

            # shutil.copy(, )

    def save_zip(self, version_info: dict[str, str]) -> str:
        version, url, zip_filename, joomla_dir_name = self.parse_info(version_info)
        zip_filepath = utils.download_zip_file(url, f"{self.output_dir}/{zip_filename}")

        extract_dst = f"{self.output_dir}/{joomla_dir_name}"

        extracted_file_names = utils.unzip_package(zip_filepath, extract_dst)
        platform_files = self.get_platform_file(extracted_file_names)

        self.copy_platform_files(joomla_dir_name, platform_files, src_dir=extract_dst)

        os.remove(zip_filepath)


# TODO sprawdzanie zawartości plików z pól

if __name__ == "__main__":
    result = PackageSaver("joomla_links.json").save_zip(
        # {
        #     "3.10.9": "https://downloads.joomla.org/cms/joomla3/3-10-9/Joomla_3-10-9-Stable-Full_Package.zip?format=zip"
        # }
        {
            "3.10.6": "https://downloads.joomla.org/cms/joomla3/3-10-6/Joomla_3-10-6-Stable-Full_Package.zip?format=zip"
        }
    )
