
import requests, re, time
from datetime import datetime
from pandas import DataFrame, read_excel, to_datetime

class _TSEShortRatio(object):

    def __init__(self):
        pass

    def get_url_of_xls_files(self, BASE_URL, URLS) -> list:

        ses = requests.Session()
        resp = ses.get(URLS['short_ratio'], timeout=6)
        resp.encoding = resp.apparent_encoding
        
        url_chars = '[0-9a-zA-Z\/\-\_]*'
        urls_xls = []
        urls_xls += re.findall('{0}\.xls?'.format(url_chars), resp.text)

        # need to scrape about 30 links on 12 months of archive pages.
        for p in re.findall('{0}\d\d-archives-\d\d\.html?'.format(url_chars), resp.text):
            resp = ses.get('{0}{1}'.format(BASE_URL, p), timeout=6)
            resp.encoding = resp.apparent_encoding
            urls_xls += re.findall('{0}\.xls?'.format(url_chars), resp.text)
            time.sleep(1)

        resp.close()
        ses.close()
       
        return list(map(lambda x: '{0}{1}'.format(BASE_URL, x), urls_xls)) 

    @staticmethod
    def get_short_ratio(self) -> dict:

        sr = _TSEShortRatio()

        urls_xls = sr.get_url_of_xls_files(self.BASE_URL, self.URLS)

        if len(urls_xls) == 0:
            raise ValueError('URL(s) of .xls files cannot be found. urls_xls has length of 0. Check start and end'.format(urls_xls))

        LABELS = {'Date of Calculation',
        'Code of Stock',
        'Name of Stock (Japanese)',
        'Name of Stock (English)',
        'Name of Short Seller',
        'Address of Short Seller',
        'Name of Discretionary Investment Contractor',
        'Address of Discretionary Investment Contractor',
        'Name of Investment Fund	Ratio of Short Positions to Shares Outstanding',
        'Number of Short Positions in Shares',
        'Number of Short Positions in Trading Units',
        'Date of Calculation in Previous Reporting',
        'Ratio of Short Positions in Previous Reporting',
        'Notes'}

        ses = requests.Session()
        res = DataFrame()
        buf = DataFrame()

        for u in urls_xls:
            print('getting {0}'.format(u))
            resp = ses.get(u, timeout=3)
            resp.encoding = resp.apparent_encoding
        
            buf = read_excel(resp.content, skiprows=7, usecols='B:P')
            buf = buf.rename(columns={'Name of Stock\n(Japanese / English)': 'Name of Stock (Japanese)',
                                    'Unnamed: 4' : 'Name of Stock (English)'})
            buf['Date of Calculation'] = to_datetime(buf['Date of Calculation'])
            res = res.append(buf)

            time.sleep(1)

        return res
