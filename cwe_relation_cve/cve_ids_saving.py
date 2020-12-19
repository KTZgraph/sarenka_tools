"""
Zapsiywanie listy wszystkich podatności cve do pliku cve_all.json (same idki)
cve_all_details.json zapisywanie dadatkowych informacji srapowanych ze strony, m.inntmi cwe id dla dane podatności
"""
import json
import time
from datetime import datetime

from cve_ids_all_nist_scraper import CVEIdsAllNistScraper


class CVEIdsSaving:
    def __init__(self):
        self.scraper = CVEIdsAllNistScraper()

    def save_all_cve_ids_to_file(self):
        starting_time = time.perf_counter()

        all_cve_ids = self.scraper.get_values()

        ending_time = time.perf_counter()

        result = {
            "created_at": str(datetime.now()),
            "performance": ending_time - starting_time,
            "cve_all": all_cve_ids
        }

        with open('cve_all.json', 'w') as fp:
            json.dump(result, fp,  indent=4)
