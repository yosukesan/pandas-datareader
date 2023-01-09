import requests, sys

from pandas import read_excel, DataFrame
from pandas_datareader.compat import string_types
from pandas_datareader.base import _BaseReader

from .short_ratio import _TSEShortRatio

class TSEReader(_BaseReader):
    """ Reader for Tokyo Stock Exchange """

    BASE_URL = 'https://www.jpx.co.jp'
    URLS = {'data_catalogue' : '{0}/markets/data-catalog/nlsgeu000005b8n0-att/datacatalogue.xlsx'.format(BASE_URL),
             'short_ratio' : '{0}/markets/public/short-selling/index.html'.format(BASE_URL),
             'margin_outstanding' : '{0}/markets/statistics-equities/margin/'.format(BASE_URL),}

    def _switch_url(self, symbols='') -> str:
        """ switch url by symbol """
        
        if not isinstance(symbols, string_types):
            raise ValueError("data name must be string")

        if not symbols in self.URLS.keys():
            raise ValueError("unknown symbol. avaliables are {0}".format(self.URLS.keys()))

        return self.URLS[symbols]

    def _get_data_catalogue(self, lang='EN') -> DataFrame:
        """ get metadata """

        # metadata (data catalogue) has data name and its URL
        # Initially considered to make key-value from them,
        # but As far as I checked some URLs specified portal page of the data

        #""" get url list of data soruces by downloading .xlsx file """

        if not lang in ['EN', 'JP']:
            raise ValueError('unknown lang={0}. Available languages are "EN", "JP"'.format(lang))

        drop_lang = 'JP'
        if lang == 'JP':
            drop_lang = 'EN' 

        _resp = requests.get(self.URLS['data_catalogue'])
        self._catalogue = read_excel(_resp.content)

        drop_keys = list(filter(lambda x: '({0})'.format(drop_lang) in x, self._catalogue.keys()))
        return self._catalogue.drop(columns=drop_keys)

    @property
    def url(self) -> str:
        import re

        if not isinstance(self.symbols, string_types):
            raise ValueError("data name must be string")

        return self._switch_url(self.symbols)

    def read(self):
        #urls_xls = _TSEShortRatio._get_url_of_xls_files(self)
        _TSEShortRatio.get_short_ratio(self)

