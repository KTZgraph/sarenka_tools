import requests
import PyPDF2
import re
import os
from functools import lru_cache


class CWEIdsExtractor:
    """Parsuje wsyzstkie kody CWE z pliku pdf https://cwe.mitre.org/data/published/cwe_latest.pdf
    tak, żeby zapisac, je do bazy danych a potem dodac im relacje z kodów CWE"""

    cwe_latest_file_url = "https://cwe.mitre.org/data/published/cwe_latest.pdf"
    CHUNK_SIZE = 8096
    START_PAGE = 3  # nadmiarowa ilosc stron na których znajdują się kody CWE
    END_PAGE = 18  # nadmiarowa ilosc stron na których znajdują się kody CWE

    def __init__(self):
        self.__local_file_path = "cwe_latest.pdf"
        self.__download_pdf()

    @property
    @lru_cache()
    def pdf_file_obj(self):
        # performance zdycha
        return self.__get_pdf_file_obj()

    @property
    def creation_date(self):
        return self.pdf_file_obj.documentInfo["/CreationDate"]

    @property
    @lru_cache()
    def cwe_ids_set(self):
        # BARDZO DLUGIE OBLICZENIA - performance zdycha
        return self.__get_all_cwes()

    def __download_pdf(self):
        response = requests.get(self.cwe_latest_file_url, stream=True)

        with open(self.__local_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                f.write(chunk)

    def __get_pdf_file_obj(self):
        pdf_file_obj = open(self.__local_file_path, "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
        return pdf_reader

    def __get_all_cwes(self):
        """Skraca plik do pierwszych 25 stron w który sa wszystkie CWE kody
        Rzowiązuje problem zbyt dużego pliku po parsowania w bibliotece pdfminer"""

        cwe_list = []
        regex = re.compile("CWE-\d+")

        for i in range(self.START_PAGE, self.END_PAGE+1):
            page_obj = self.pdf_file_obj.getPage(i)
            page_str = page_obj.extractText()
            cwe_list.extend(regex.findall(page_str))

        return set(cwe_list)


if __name__ == "__main__":
    parser = CWEIdsExtractor()
    # parser.download_pdf()
    # print(parser.cwe_ids_set)
