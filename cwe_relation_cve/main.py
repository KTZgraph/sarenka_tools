"""
1. Pobierz wszystkie kody CWE - ich id oraz opis, zapisz je do pliku json

"""


from cwe_ids_saving import CWEIdsSaving


def save_all_cwe():
    cwe_ids_saving = CWEIdsSaving()
    cwe_ids_saving.save_to_file()


if __name__ == "__main__":
    save_all_cwe()
