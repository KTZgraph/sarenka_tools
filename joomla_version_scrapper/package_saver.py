import utils
import os

class PackageSaver:
    def __init__(self, filepath:str, output_dir:str="output_joomla") -> None:
        self.data = utils.get_dict_from_json_file(filepath)
        self.output_dir = output_dir
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)


    def save_zip(self, version_info:dict[str, str])->str:
        result = []
        for k, v in version_info.items():
            version_number = k
            link = v
            zip_filename = v.split('/')[-1].split('?')[0]
            extracted_dirname = zip_filename.split(".")[0]

            zip_filepath= utils.download_zip_file(
                URL=link, filename=f"{self.output_dir}/{zip_filename}"
            )

            print(zip_filepath)
            extract_destination = f"{self.output_dir}/{extracted_dirname}"
            if not os.path.isdir(self.output_dir):
                os.mkdir(self.output_dir)

            extracted_file_names = utils.unzip_package(zip_filepath, extract_destination)
            os.remove(zip_filepath)
            result.append({
                "version": version_number,
                "url" : link,
                "zip": zip_filename,
                "filename": extracted_file_names[0]  # tylko jeden plik w zipie

            })

        return result


if __name__ == "__main__":
    result = PackageSaver("joomla_links.json").save_zip({
        "3.10.9": "https://downloads.joomla.org/cms/joomla3/3-10-9/Joomla_3-10-9-Stable-Full_Package.zip?format=zip"
    })

    # print(result)

    # zip_filepath = utils.download_zip_file(
    #     URL="https://downloads.joomla.org/cms/joomla3/3-10-9/Joomla_3-10-9-Stable-Full_Package.zip?format=zip",
    #     filename=f"output/Joomla_3-10-9-Stable-Full_Package.zip")
    

    