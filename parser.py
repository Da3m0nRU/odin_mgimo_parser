import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://lka.mgimo.ru/upload/sp/spospi%20(HTML).html'

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'accept':
	'*/*' }
#Заголовки - объявляем их для того, чтобы сайт не принял нас за бота.

FILE = 'Список_колледж.csv'

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
    find_date = soup.find_all('td', class_='R3C0')

    date_of_formation = []
    for date in find_date:
        date_of_formation.append(date.get_text(strip = True))

    applicants = []
    for item in items:
        if (item.find('td', class_='R12C2') != None):
            applicants.append({
                'ФИО': item.find('td', class_='R12C2').get_text(strip = True),
                #strip - убирание пробелов спереди и сзади, get_text - получение текста только между тегами
                'Средний_балл': item.find('span').get_text(strip = True)
            })

    return applicants, date_of_formation

def save_file(items, path, date_of_formation):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Список поданных заявлений: Колледж'])
        writer.writerow([date_of_formation[0], date_of_formation[1]])
        writer.writerow(['ФИО', 'Средний балл'])
        for item in items:
            writer.writerow([item['ФИО'], item['Средний_балл']])


def parse():
    html = get_html(URL)
    #передаём в html то, что получили с запроса
    #print(html.status_code)
    #Выводим ответ от сайта, если 200 - то всё ок.
    if html.status_code == 200:
        applicants, date_of_formation = get_content(html.text)
        save_file(applicants, FILE, date_of_formation)
        print(applicants)
        print("Количество абитуриентов: " + str(len(applicants)))
        print(date_of_formation)
    else:
        print("Ошибка!")

parse()
