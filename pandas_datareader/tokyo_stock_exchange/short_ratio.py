
import requests, re, time
from datetime import datetime
from pandas import DataFrame, read_excel, to_datetime

class _TSEShortRatio(object):

    def __init__(self):
        pass

    def get_url_of_xls_files(self) -> list:

        ses = requests.Session()
        BASE_URL = 'https://www.jpx.co.jp'
        URL = '{0}/markets/public/short-selling/index.html'.format(BASE_URL)
        resp = ses.get(URL, timeout=6)
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

    def filter_xls_url_by_period(self, urls_xls: list, start: datetime, end: datetime):

        hm = {}
        pattern = re.compile('\d{8}_')

        for j in urls_xls:
            res = re.search(pattern, j)
            date = datetime.strptime(res.group()[:-1], '%Y%m%d')
            hm[date] = j

        new_urls_xls = []
        for d in hm.keys():  
            if start <= d and d <= end:
                new_urls_xls.append(hm[d])

        return new_urls_xls

    def get(self, start: datetime, end: datetime) -> dict:

        sr = _TSEShortRatio()

        urls_xls = sr.get_url_of_xls_files()
        urls_xls = sr.filter_xls_url_by_period(urls_xls, start, end)

        if len(urls_xls) == 0:
            raise ValueError('URL(s) of .xls files cannot be found. urls_xls has length of 0. Check start and end')

        ses = requests.Session()
        res = DataFrame()
        buf = DataFrame()

        print('Getting...')
        for u in urls_xls:
            print(u)
            resp = ses.get(u, timeout=3)

            # Shift-JIS to UTF-8
            resp.encoding = resp.apparent_encoding
        
            buf = read_excel(resp.content, skiprows=7, usecols='B:P')
            buf = buf.rename(columns={'Name of Stock\n(Japanese / English)': 'Name of Stock (Japanese)',
                                    'Unnamed: 4' : 'Name of Stock (English)'})
            buf['Date of Calculation'] = to_datetime(buf['Date of Calculation'])
            res = res.append(buf)

            time.sleep(1)

        return res
