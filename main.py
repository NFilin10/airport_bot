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


#получение данных для корректного запроса на сайт, чтобы получить билеты (еще не готово)
def get_nonce():
    url = "https://www.tallinn-airport.ee/lennuinfo/sihtkohad/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    form = soup.find('form', class_='form')
    nonce = form.find_all('input', id='_wpnonce')
    for i in nonce:
        nonce = i.get('value')
    return nonce



def get_dest_airport_name():
    url = 'https://www.tallinn-airport.ee/findflight.php?language=et&term=Antalya'
    pg = requests.get(url)
    content = json.loads(pg.text)
    airport = content[0]["value"]
    return airport


def get_tickets_link():
    payload = {
        'goToSearch': '1',
        'language': 'et',
        '_wpnonce': get_nonce(),
        '_wp_http_referer': '/lennuinfo/sihtkohad/',
        'action': 'search_flight_form_submit',
        'flightFrom': 'Tallinn, Lennart Meri (TLL) - Eesti',
        'flightTo': get_dest_airport_name(), #change this
        'startDate': '05.11.2022', #change this
        'backDate': '11.11.2022', #change this
        'adults': '1', #change this
        'children': '0', #change this
        'infants': '0', #change this
    }

    url = "https://www.tallinn-airport.ee/wp-admin/admin-ajax.php"
    page = requests.post(url, data=payload)
    content = json.loads(page.text)
    ticket_link = content['data'].replace("\\", "")
    print(ticket_link)
get_tickets_link()




