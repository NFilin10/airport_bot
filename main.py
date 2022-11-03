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

#получение доступных рейсов в выбранную дату
def sihtkohad(direction):
    sihkoht = "Riia"  #input("Sisesta sihtkoht: ")
    date = input("Sisesta lennu kuupäev: ")

    sihtkoha_id = get_country_indexes()[sihkoht]
    #page = requests.get("https://www.tallinn-airport.ee/lennuinfo/sihtkohad/#/s=" + sihkoht)

    payload = {
        'action': 'adm_get_flights_by_date',
        'id': sihtkoha_id,
        'date': date,
        'direction': direction,
        'language': 'et'
    }

    flights = requests.post("https://www.tallinn-airport.ee/wp-admin/admin-ajax.php", data=payload)
    flight_info = json.loads(flights.text)

    print("On olemas järgmised lennud:")
    for i in range(0, len(flight_info)):
        print(f"Sihtkoht: {flight_info[i]['name']}\nVäljumine: {flight_info[i]['timeDepartureFormatted']}\n"
              f"Saabumine: {flight_info[i]['timeArrivalFormatted']}\nKestvus: {flight_info[i]['durationInHours']}\n"
              f"Lennufirma: {flight_info[i]['airlines'][0]['name']}\nLennu nr: {flight_info[i]['airlines'][0]['nr']}\n")


