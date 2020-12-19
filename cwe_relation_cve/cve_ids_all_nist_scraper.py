import requests
from bs4 import BeautifulSoup


class CVEIdsAllNistScraper:

    full_listing_url = "https://nvd.nist.gov/vuln/full-listing"
    main_url = "https://nvd.nist.gov"

    def __init__(self):
        self.__all_cves = self.get_values()

    @property
    def all_cves(self):
        return self.__all_cves

    def __get_year_month_hrefs(self):
        """1. Krok scrapowania"""
        result = []
        source = requests.get(self.full_listing_url).text
        soup = BeautifulSoup(source, 'lxml')

        span_list = soup.findAll("span")
        for span in span_list:
            href_list = span.findAll("a")
            for a in href_list:
                href = a.get("href", None)
                if href and "/vuln/full-listing/" in href:
                    result.append(a["href"])

        return result

    def __get_cves_codes_by_year_month(self, year_month_url):
        """2. Krok scrapowanie - wyciagnięcie samych kodów cve z  urla po miesiacu"""
        result = []
        source = requests.get(self.main_url + year_month_url).text
        soup = BeautifulSoup(source, 'lxml')
        span_list = soup.findAll("span", {"class": "col-md-2"})
        for span in span_list:
            a = span.find("a")
            result.append(a.text)

        return result

    def get_values(self):
        result = []
        year_month_hrefs = self.__get_year_month_hrefs()
        for y_m_url in year_month_hrefs:
            year, month = y_m_url.split("/")[-2:]
            for cve_code in self.__get_cves_codes_by_year_month(y_m_url):
                result.append({
                    "cve_code": cve_code,
                    "year": year,
                    "month": month
                }
                )

        return result
