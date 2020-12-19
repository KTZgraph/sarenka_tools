import json
from cwe_ids_extractor import CWEIdsExtractor
from cwe_mitre_scrapper import CWEMitreScraper
from cwe_wrapper import CWEWrapper


class CWEIdsSaving:
    def __init__(self):
        self.__cwe_ids_extractor = CWEIdsExtractor()

    @property
    def cwe_db_timestamp(self):
        return self.__cwe_ids_extractor.creation_date

    @property
    def all_cwes_ids(self):
        return self.__cwe_ids_extractor.cwe_ids_set

    def get_data(self):
        result = []
        for cwe_id in self.all_cwes_ids:
            result.append(
                CWEWrapper(
                    cwe_id=cwe_id,
                    # description=CWEMitreScraper(cwe_id).get_description()
                    description="No description"
                )
            )

        return result

    def save_to_file(self):
        cwe_all = []
        for cwe in self.get_data():
            cwe_all.append(cwe.values)

        result = {"timestamp": self.cwe_db_timestamp, "cwe_all": cwe_all}

        with open('cwe_all.json', 'w') as fp:
            json.dump(result, fp,  indent=4)
