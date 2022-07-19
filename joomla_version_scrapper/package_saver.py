import utils
import os
import shutil
class PackageSaver:
    def __init__(self, filepath:str, output_dir:str="output_joomla") -> None:
        self.data = utils.get_dict_from_json_file(filepath)
        self.output_dir = output_dir
        self.platform_files = "joomla_platform"
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

    def get_platform_file(self, extracted_files_info:list[str]):
        platform_files = []
        for filepath in extracted_files_info:
            if "platform.php" in filepath:
                platform_files.append(filepath)
        return platform_files 

    def copy_platform_files(self, platform_files:list[str], src_dir:str,  dst_dir:str)->list[str]:
        for src_path in platform_files:
            print("src: ", f"{src_dir}/{src_path}")
            print("dst: ", f"{dst_dir}/platform.php")

            # shutil.copy(, )

    def parse_info(self, version_info:dict[str, str])->dict[str, str]:
        for version_number, url in version_info.items():
            zip_filename = url.split('/')[-1].split('?')[0]
            extracted_dirname=  zip_filename.split(".")[0]

            return version_number, url, zip_filename, extracted_dirname

    def save_zip(self, version_info:dict[str, str])->str:
        version, url, zip_filename, extracted_dirname = self.parse_info(version_info)

        result = []

        zip_filepath= utils.download_zip_file(
            url, f"{self.output_dir}/{zip_filename}"
        )
        extract_destination = f"{self.output_dir}/{extracted_dirname}"
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        extracted_file_names = utils.unzip_package(zip_filepath, extract_destination)
        platform_files = self.get_platform_file(extracted_file_names)
        # utils.save_dict_as_json(extracted_file_names, "joomla_3-10-9.json")

        self.copy_platform_files(platform_files, src_dir=extract_destination, dst_dir=f"{self.platform_files}/{extracted_dirname}")

        os.remove(zip_filepath)
        result.append({
            "version": version,
            "url" : url,
            "zip": zip_filename,
            "filename": platform_files  # tylko jeden plik w zipie

        })

        return result


if __name__ == "__main__":
    result = PackageSaver("joomla_links.json").save_zip({
        "3.10.9": "https://downloads.joomla.org/cms/joomla3/3-10-9/Joomla_3-10-9-Stable-Full_Package.zip?format=zip"
    })

    