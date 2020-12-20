"""
Kopiowanie plików
┌──────────────────┬────────┬───────────┬──────────┬────────────────┐
│     Function     │ Copies │   Copies  │ Use file │   Destination  │
│                  │metadata│permissions│  object  │may be directory│
├──────────────────┼────────┼───────────┼──────────┼────────────────┤
│shutil.copy       │   No   │    Yes    │    No    │      Yes       │
│shutil.copyfile   │   No   │     No    │    No    │       No       │
│shutil.copy2      │  Yes   │    Yes    │    No    │      Yes       │
│shutil.copyfileobj│   No   │     No    │   Yes    │       No       │
└──────────────────┴────────┴───────────┴──────────┴────────────────┘


CWE_DB_PATH = os.path.join(BASE_DIR,'cwe_databases')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },

    'CWE_NONE': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'cwe_none.sqlite3'),
    },

    'CWE_209': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(CWE_DB_PATH, 'cwe_209.sqlite3'),
    },

"""
import json
from shutil import copy2
import os


class ManyDatabasesGenerator:
    def __init__(self):
        self.__all_cwe_file = "cwe_all.json"
        self.__folder_name = "cwe_databases"
        self.__all_cwe_ids = self.get_all_cwe_ids()
        self.source = "db.sqlite3"

    @property
    def all_cwe_ids(self):
        return self.__all_cwe_ids 

    @property
    def folder_name(self):
        return self.__folder_name

    @property
    def all_cwe_file(self):
        return self.__all_cwe_file


    def get_all_cwe_ids(self):
        """
        Zwraca wszystkie id CWE kodów
        """
        with open(self.all_cwe_file) as json_file:
            data = json.load(json_file)

        all_cwes = data["cwe_all"]
        all_cwes_ids =  [i["cwe_id"] for i in all_cwes]
        all_cwes_ids.append("CWE-NONE") # dla tych CVe co nie mają CWE
        return all_cwes_ids

    def get_file_destination(self, cwe_id):
        name = cwe_id.replace("-", "_").lower()
        filename =  name + "." + self.source.split(".")[-1]
        destination = self.folder_name + "\\"  + filename
        return destination


    def copy_files(self):
        for cwe_id in self.all_cwe_ids:
            dest = self.get_file_destination(cwe_id)
            # copyfile(self.source, dest)
            copy2(self.source, dest) # kopiuje METADANE

    def get_django_config_dbs(self):
        result = """
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            },
        """

        PART_CONST_START = """ :{
                'ENGINE': 'django.db.backends.sqlite3',
                """

        PART_CONST_END = """'),
            },
        """

        print(self.all_cwe_ids)

        for cwe_id in self.all_cwe_ids:
            cwe_part = f"""
            '{cwe_id.replace("-", "_")}'"""

            result += cwe_part
            result += PART_CONST_START

            db_part = f"""'NAME': os.path.join(CWE_DB_PATH, '{cwe_id.replace("-", "_").lower()}.sqlite3"""
            result += db_part
            result += PART_CONST_END

        result += "\n}"

        self.save_as_txt(result)

        print(result)
        return result

    def save_as_txt(self, generated_str):
        with open("django_settings.txt", "w") as f:
            f.write(generated_str)



if __name__ == "__main__":
    generator = ManyDatabasesGenerator()
    # generator.copy_files()
    # print(generator.get_django_config_dbs())
    print(len(generator.all_cwe_ids))
