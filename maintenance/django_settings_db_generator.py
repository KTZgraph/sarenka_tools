"""
Do generowanie słwonika dla ustawień
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    

}

"""
import os
import json


class DjangoSettingsDbGenerator:
    file_name = "cwe_all.json"

    def __init__(self):
        self.__cwe_ids_filepath = self.__get_filepath()

    def __get_filepath(self):
        one_up = os.path.abspath(os.path.join(__file__, "../.."))
        return os.path.join(one_up, self.file_name)

    def __get_all_cwe_codes(self):
        with open(self.__cwe_ids_filepath) as json_file:
            data = json.load(json_file)

        return data["cwe_all"]

    def save_as_txt(self, generated_str):
        with open("django_settings.txt", "w") as f:
            f.write(generated_str)

    def generate(self):
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

        all_cwes = self.__get_all_cwe_codes()
        # bo są takie podatnosci bez CWE;a nie chę używac domyślnej bazy
        all_cwes.append({"cwe_id": "CWE-NONE"})

        print(len(all_cwes))

        for cwe in all_cwes:
            cwe_part = f"""
            '{cwe["cwe_id"].replace("-", "_")}'"""

            result += cwe_part
            result += PART_CONST_START

            db_part = f"""'NAME': os.path.join(BASE_DIR, '{cwe["cwe_id"].replace("-", "_").lower()}.sqlite3"""
            result += db_part
            result += PART_CONST_END

        result += "\n}"

        self.save_as_txt(result)

        # print(result)
        return result


if __name__ == "__main__":
    DjangoSettingsDbGenerator().generate()
