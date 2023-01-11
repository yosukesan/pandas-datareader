
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
        df2 = web.get_data_tse("short_ratio", start=start, end=end)

        assert df.keys()[0] == 'Date of Calculation'
        assert df2.keys()[0] == 'Date of Calculation'

    def test_symbol(self):
        """ check if wrong symbol captures error termination """

        start = datetime.today() - relativedelta(day=3)
        delta = relativedelta(day=4)
        end = start - delta

        # This intentionally has white space
        wrong_symbol = '  xxdfdf_/.~  '

        with pytest.raises(ValueError) as wrong_str:
            web.DataReader(wrong_symbol, "tse", start, end)

        with pytest.raises(ValueError) as int_arg:
            web.DataReader(1, "tse", start, end)

        assert str(wrong_str.value) == "symbol does not exist."
        assert str(int_arg.value) == "data name must be string"

    def test_single_day(self):
        """ check if start == end returns single day """

        start = datetime.today() - relativedelta(day=3)
        end = start

        df = web.DataReader('data_catalogue', "tse", start, end)
        df2 = web.get_data_tse('data_catalogue', start, end)
        assert df.keys()[0] == 'ServiceID'
        assert df2.keys()[0] == 'ServiceID'

    def test_if_upstream_data_doesnt_exist(self):
        """
            TSE is closed for Jan 1st to Jan 2nd.
            Upstream does not have data in this period.
        """

        this_year = datetime.today()
        start = datetime(int(this_year.strftime('%Y')), 1, 1)
        end = datetime(int(this_year.strftime('%Y')), 1, 2)

        with pytest.raises(ValueError) as e:
            web.DataReader('short_ratio', "tse", start, end)

        return str(e.value) == 'URL(s) of .xls files cannot be found. urls_xls has length of 0. Check start and end'
