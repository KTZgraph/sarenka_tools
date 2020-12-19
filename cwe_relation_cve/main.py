"""
1. Pobierz wszystkie kody CWE, pobierz wszsytkie opisy słabości - ich id oraz opis, zapisz je do pliku json


"""


from cwe_ids_saving import CWEIdsSaving
from cve_ids_saving import CVEIdsSaving


def save_all_cwe():
    """
    1. Grabs data from official mitre file "https://cwe.mitre.org/data/published/cwe_latest.pdf".
    2. Scrap description by cwe ids from  "https://cwe.mitre.org/"
    3. Saves data to json.file "cwe_all.json" 
    """
    pass
    # cwe_ids_saving = CWEIdsSaving()
    # cwe_ids_saving.save_to_file()


def save_all_cve_ids():
    cve_all_saving = CVEIdsSaving()
    cve_all_saving.save_all_cve_ids_to_file()


if __name__ == "__main__":
    # save_all_cwe()
    save_all_cve_ids()
