
from datetime import datetime
from dateutil.relativedelta import relativedelta

from pandas_datareader import data as web
from pandas_datareader._utils import RemoteDataError

class TestTSE:

    def test_short_ratio(self):

        start = datetime.today() - relativedelta(day=3)
        delta = relativedelta(day=365)
        end = start - delta 

        df = web.DataReader("short_ratio", "tse", start, end)
