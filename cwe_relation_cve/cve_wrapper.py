class CVEWrapper:
    def __init__(self, cve, year, month, cwe=None):
        """

        :param cve:
        :param year:
        :param month:
        :param cwe:
        """
        self.__cve = cve
        self.__year = year
        self.__month = month
        self.__cwe = cwe

    @property
    def cve(self):
        return self.__cve

    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def cwe(self):
        return self.__cwe

    @cwe.setter
    def cwe(self):
        return self.__cwe

    @cwe.deleter
    def cwe(self):
        return self.__cwe
