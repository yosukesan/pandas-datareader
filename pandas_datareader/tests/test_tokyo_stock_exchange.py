
import pytest

from datetime import datetime
from dateutil.relativedelta import relativedelta

from pandas_datareader import data as web

class TestTSE:

    def test_interval(self):

        start = datetime.today() - relativedelta(day=3)
        delta = relativedelta(day=4)
        end = start - delta 

        df = web.DataReader("short_ratio", "tse", start, end)

        assert df.keys()[0] == 'Date of Calculation'

    def test_symbol(self): 
        """ check if wrong symbol captures error termination """

        start = datetime.today() - relativedelta(day=3)
        delta = relativedelta(day=4)
        end = start - delta 

        # This intentionally has white space
        wrong_symbol = '  xxdfdf_/\.~  '

        with pytest.raises(ValueError) as wrong_str:
            df = web.DataReader(wrong_symbol, "tse", start, end)

        with pytest.raises(ValueError) as int_arg:
            df = web.DataReader(1, "tse", start, end)

        assert str(wrong_str.value) == "symbol does not exist."
        assert str(int_arg.value) == "data name must be string"

    def test_single_day(self):
        """ check if start == end returns single day """

        start = datetime.today() - relativedelta(day=3)
        end = start

        df = web.DataReader('data_catalogue', "tse", start, end)
        assert df.keys()[0] == 'ServiceID'

    def test_if_upstream_data_doesnt_exist(self):
        """
            TSE is closed for Jan 1st to Jan 2nd.
            Upstream does not have data in this period.
        """

        this_year = datetime.today()
        start = datetime(int(this_year.strftime('%Y')),1,1)
        end = datetime(int(this_year.strftime('%Y')),1,2)
