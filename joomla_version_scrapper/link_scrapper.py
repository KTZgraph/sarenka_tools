import requests
from bs4 import BeautifulSoup
import utils
import os


class LinkScrapper:
    MAIN_URL = "https://downloads.joomla.org"
    JOOMLA_2_5_URL = "https://downloads.joomla.org/cms/joomla25"
    JOOMLA_3_X_URL = "https://downloads.joomla.org/cms/joomla3"
    JOOMLA_4_URL = "https://downloads.joomla.org/cms/joomla4"

    def __init__(self) -> None:
        self.url_list = [
            LinkScrapper.JOOMLA_3_X_URL,
            LinkScrapper.JOOMLA_2_5_URL,
            LinkScrapper.JOOMLA_4_URL,
        ]
        self.file_output = "joomla_links.json"

        if os.path.isfile(self.file_output):
            self.url_list = utils.get_dict_from_json_file(
                filepath=self.file_output)
        else:
            self.url_list = self.get_general_joomla_links()
            utils.save_dict_as_json(
                data=self.url_list, filename=self.file_output)

    def get_zip_package(self, version_url: str) -> str:
        """Zwraca string z linkie do konkrentej wersji"""
        source = requests.get(version_url).text
        soup = BeautifulSoup(source, "html.parser")

        for a in soup.find_all("a", href=True, class_="btn btn-primary"):
            if "zip" in a["href"] and "update" not in a["href"]:
                return f'{LinkScrapper.MAIN_URL}{a["href"]}'

    def get_general_joomla_links(self) -> list[str]:
        """Pobiera linki z głównej strony do wersji joomli."""
        version_url_list = []
        for url in self.url_list:
            source = requests.get(url).text
            soup = BeautifulSoup(source, "html.parser")

            for a in soup.find_all("a", href=True, class_="btn btn-primary"):
                href = f'{LinkScrapper.MAIN_URL}{a["href"]}'
                version_info = a["href"].split("/")[-1].replace("-", ".")
                package_url = self.get_zip_package(href)
                version_url_list.append({version_info: package_url})

        return version_url_list
