class CWEWrapper:
    def __init__(self, cwe_id, description):
        self.__cwe_id = cwe_id
        self.__description = description
        self.__cve_ids_list = []

    def add_cve(self, cve_id):
        self.__cve_ids_list.extend(cve_id)

    @property
    def cve_ids(self):
        return self.__cve_ids_list

    @property
    def cwe_id(self):
        return self.__cwe_id

    @property
    def description(self):
        return self.__description

    def __str__(self):
        return f"CWE_ID: {self.cwe_id}\nDescription: {self.description}"

    @property
    def values(self):
        return {"cwe_id": self.cwe_id, "description": self.description}
