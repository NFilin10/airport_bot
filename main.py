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

