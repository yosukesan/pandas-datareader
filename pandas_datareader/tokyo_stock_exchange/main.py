import requests, sys

from pandas import DataFrame
from pandas_datareader.compat import string_types
from pandas_datareader.base import _BaseReader

from .data_catalogue import _TSEDataCatalogue
from .short_ratio import _TSEShortRatio

class TSEReader(_BaseReader):
    """ Reader for Tokyo Stock Exchange """

    def read(self) -> DataFrame:

        if not isinstance(self.symbols, string_types):
            raise ValueError("data name must be string")

        # remove unrequired white space(s) or tabs
        self.symbols = self.symbols.strip()

        target = {'data_catalogue': _TSEDataCatalogue(),
                  'short_ratio': _TSEShortRatio()}

        if not self.symbols in target.keys():
            print('Avaiable symbols: {0}'.format(target.keys()), file=sys.stderr)
            raise ValueError("symbol does not exist.")

        return target[self.symbols].get(self.start, self.end)
