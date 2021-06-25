import requests
from bs4 import BeautifulSoup

URL = 'https://lka.mgimo.ru/upload/sp/spospi%20(HTML).html'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'accept':
	'*/*' }
#Заголовки - объявляем их для того, чтобы сайт не принял нас за бота.

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    # отправляем запрос на сайт
    r.encoding = 'utf-8'
    #меняем кодировку для русских символов
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Создание объекта модуля beatifulsoup
    items = soup.find_all('tr', class_='R3')

    applicants = []
    for item in items:
        if (item.find('td', class_='R12C2') != None):
            applicants.append({
                'Applicant name': item.find('td', class_='R12C2').get_text(strip = True),
                #strip - убирание пробелов спереди и сзади, get_text - получение текста только между тегами
                'Average score': item.find('span').get_text(strip = True)
            })

    print(applicants)
    print(len(applicants))

def parse():
    html = get_html(URL)
    #передаём в html то, что получили с запроса
    #print(html.status_code)
    #Выводим ответ от сайта, если 200 - то всё ок.
    if html.status_code == 200:
        get_content(html.text)
    else:
        print("Ошибка!")

parse()
