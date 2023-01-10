
import requests
from pandas import read_excel, DataFrame

class _TSEDataCatalogue:

    def get(self, *argc, **kwargs) -> DataFrame:
        """ get metadata """

        URL = 'https://www.jpx.co.jp/markets/data-catalog/nlsgeu000005b8n0-att/datacatalogue.xlsx'

        _resp = requests.get(URL)
        self._catalogue = read_excel(_resp.content)

        return self._catalogue
