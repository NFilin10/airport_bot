from bs4 import BeautifulSoup
import requests
import json

#Получание всех вылетов (таблица, которая нахолится в переменной url)
def get_all_departures():
    url = "https://www.tallinn-airport.ee/lennuinfo/reaalaja-lennuinfo/?type=departures"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    a = []

    columns = soup.find_all('td')

    for i in columns:
        a.append(i.text.replace("\n", "").replace("\t", ""))

    b = []

    x = 0
    y = 5
    for i in a:
        b.append(a[x:y])
        x += 5
        y += 5
    print(b)

#получение индексов каждой страны, чтобы можно было определять какая страна интересует пользователя
def get_country_indexes():
    url = "https://www.tallinn-airport.ee/lennuinfo/sihtkohad/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ids = soup.find_all('li', class_='destination-item')

    country_data = {}
    for id in ids:
        country_name = id.text.strip()
        country_id = id.get('data-destination')
        country_data[country_name] = country_id
    return country_data


