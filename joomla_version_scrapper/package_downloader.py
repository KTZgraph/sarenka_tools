from struct import pack
import requests
from bs4 import BeautifulSoup
import os
import utils

class PackageDownloader:
    MAIN_URL = "https://downloads.joomla.org"
    joomla_3_x_url = "https://downloads.joomla.org/cms/joomla3"
    joomla_2_5 = "https://downloads.joomla.org/cms/joomla25"
    joomla_4 = "https://downloads.joomla.org/cms/joomla4"

    def __init__(self) -> None:
        self.version_zip_urls = self.get_version_zip_links([PackageDownloader.joomla_3_x_url, PackageDownloader.joomla_2_5, PackageDownloader.joomla_4]) 

    def get_zip_package(self, version_url:str)->str:
        source = requests.get(version_url).text
        soup = BeautifulSoup(source, "html.parser")

        for a in soup.find_all("a", href=True, class_="btn btn-primary"):
            if "zip" in a["href"] and "update" not in a["href"]:
                return f'{PackageDownloader.MAIN_URL}{a["href"]}'

    def get_version_zip_links(self, url_list:list[str])->list[dict[str, str]]:
        files_urls = []
        for url in url_list:
            source = requests.get(url).text
            soup = BeautifulSoup(source, "html.parser")

            for a in soup.find_all("a", href=True, class_="btn btn-primary"):
                href = f'{PackageDownloader.MAIN_URL}{a["href"]}'
                version_info = a["href"].split("/")[-1].replace("-", ".")
                package_url = self.get_zip_package(href)
                print(package_url)
                files_urls.append({ version_info: package_url })

        return files_urls




if __name__ == "__main__":
    zip_list = PackageDownloader().version_zip_urls
    print(zip_list)
    utils.save_dict_as_json(zip_list, "joomla_links.json")
