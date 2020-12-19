"""
1. Pobierz wszystkie kody CWE - ich id oraz opis, zapisz je do pliku json

"""
import time

from cwe_ids_saving import CWEIdsSaving


def save_all_cwe():
    starting_time = time.perf_counter()
    cwe_ids_saving = CWEIdsSaving()
    cwe_ids_saving.save_to_file()
    ending_time = time.perf_counter()
    print("CWE saver performance: ", ending_time - starting_time)


if __name__ == "__main__":
    save_all_cwe()
