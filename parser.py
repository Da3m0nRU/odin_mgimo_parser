import requests
from bs4 import BeautifulSoup

URL = 'https://lka.mgimo.ru/upload/sp/spospi%20(HTML).html'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'accept':
	'*/*' }
#Заголовки - объявляем их для того, чтобы сайт не принял нас за бота.

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def parse():
    html = get_html(URL)
    print(html.status_code)
    if html.status_code == 200:
        print(html.text)
    else:
        print("Ошибка!")

parse()
