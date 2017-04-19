import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://www.12306.cn/mormhweb/kyyyz/'
    try:
        s = requests.get(url)
    except Exception ,e:
        print 'requests url fail.' + url
        raise e
    b = BeautifulSoup(s.content,'lxml')
    results = b.select('#secTable > tbody > tr > td')

    for result in results:
        print result.text
