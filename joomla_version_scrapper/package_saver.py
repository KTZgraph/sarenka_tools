import utils
import os
import shutil


class PackageSaver:
    def __init__(self, src_filepath: str) -> None:
        self.url_list: list[dict[str, str]
                            ] = utils.get_dict_from_json_file(src_filepath)
        self.tmp_dir = "output_tmp"
        self.dst_dir = "output_joomla"
        utils.create_dir_if_not_exists(self.tmp_dir)
        utils.create_dir_if_not_exists(self.dst_dir)

        self.save()

    def save(self):
        # FIXME zrobić dla całej listy
        for element in self.url_list[:2]:
            for version, link in element.items():
                print(version, link)
                # zip_filepath = "Joomla_3-10-10-Stable-Full_Package.zip"
                zip_filepath = self.downlad_zip(link)
                # Joomla_3-10-10-Stable-Full_Package
                unpacked_fileapth = zip_filepath.split(".")[0]
                files = utils.unzip_package(zip_filepath, unpacked_fileapth)
                os.remove(zip_filepath)

                platform_filepaths = self.get_platform_files(
                    files)  # tylko pliki platform
                self.save_platform_files(unpacked_fileapth, platform_filepaths)
                # usuwanie na końcu pobranych rzeczy
                os.remove(unpacked_fileapth)

    def save_platform_files(self, unpacked_fileapth: str,  platform_files: list[str]):
        for p_filepath in platform_files:
            # tworzenie folderu na wyakowaną joomle
            utils.create_dir_if_not_exists(unpacked_fileapth)
            concrete_joomla_dir = unpacked_fileapth.split('/')[-1]
            # print("concrete_joomla_dir: ", concrete_joomla_dir)

            structure = utils.get_folder_structure(p_filepath)
            structure = [
                f"{self.dst_dir}/{concrete_joomla_dir}/{i}" for i in structure]

            structure.insert(0, f"{self.dst_dir}/{concrete_joomla_dir}")
            structure.insert(0, self.dst_dir)

            utils.create_folder_structure(structure)

            final_src_filepath = f"{self.tmp_dir}/{concrete_joomla_dir}/{p_filepath}"
            final_dst_filepath = f"{self.dst_dir}/{concrete_joomla_dir}/{p_filepath}"

            shutil.copy2(final_src_filepath, final_dst_filepath)

    def downlad_zip(self, URL: str) -> str:
        filename = URL.split("/")[-1].split('?')[0]
        dst_filepath = f"{self.tmp_dir}/{filename}"
        utils.download_zip_file(URL, dst_filepath)
        return dst_filepath

    def get_platform_files(self, extracted_files_info: list[str]):
        # w plikach platform.php są informację o wersjach
        platform_files = []
        for filepath in extracted_files_info:
            if "platform.php" in filepath:
                platform_files.append(filepath)
        return platform_files


if __name__ == "__main__":
    PackageSaver("joomla_links.json")
