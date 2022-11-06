import time

from bs4 import BeautifulSoup
import requests
import json
import datetime

#Получание всех вылетов (таблица, которая нахолится в переменной url)
def get_all_departures():
    url = "https://www.tallinn-airport.ee/lennuinfo/reaalaja-lennuinfo/?type=departures"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    terve_tabel = []

    read = soup.find_all('td')

    for rida in read:
        terve_tabel.append(rida.text.replace("\n", "").replace("\t", ""))

    all_departures = []
    index1 = 0
    index2 = 5
    for i in terve_tabel:
        all_departures.append(terve_tabel[index1:index2])
        index1 += 5
        index2 += 5

    times = []

    sihtkoht = "Riga"

    for i in range(0, len(all_departures)):
        for j in range(0, len(all_departures[i])):
            if sihtkoht in all_departures[i][j]:
                time = [all_departures[i][0], all_departures[i][-1]]
                if "Saabus" in time[1] or time[1] == '':
                    continue
                else:
                    times.append(time)
    print(times)




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
def sihtkohad(direction, sihtkoht, date):

    sihtkoha_id = get_country_indexes()[sihtkoht]

    payload = {
        'action': 'adm_get_flights_by_date',
        'id': sihtkoha_id,
        'date': date,
        'direction': direction,
        'language': 'et'
    }

    flights = requests.post("https://www.tallinn-airport.ee/wp-admin/admin-ajax.php", data=payload)
    flight_info = json.loads(flights.text)

    lennud = []

    for i in range(0, len(flight_info)):
        lennud.append(f"Sihtkoht: {flight_info[i]['name']}\nVäljumine: {flight_info[i]['timeDepartureFormatted']}\n"
              f"Saabumine: {flight_info[i]['timeArrivalFormatted']}\nKestvus: {flight_info[i]['durationInHours']}\n"
              f"Lennufirma: {flight_info[i]['airlines'][0]['name']}\nLennu nr: {flight_info[i]['airlines'][0]['nr']}\n")
    return "\n".join(lennud)

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



def get_dest_airport_name(sihtkoht):
    url = 'https://www.tallinn-airport.ee/findflight.php?language=et&term=' + sihtkoht.capitalize()
    pg = requests.get(url)
    content = json.loads(pg.text)
    airport = content[0]["value"]
    return airport


def get_tickets_link(sihtkoht, kuupaev, suund, tagasi_lend, adults, children, pens, suund1):
    payload = {
        'goToSearch': '1',
        'language': 'et',
        '_wpnonce': get_nonce(),
        '_wp_http_referer': '/lennuinfo/sihtkohad/',
        'action': 'search_flight_form_submit',
        'flightFrom': 'Tallinn, Lennart Meri (TLL) - Eesti',
        'flightTo': get_dest_airport_name(sihtkoht),
        'oneWay': suund,
        'startDate': kuupaev, #change this
        'backDate': tagasi_lend, #change this
        'adults': adults, #change this
        'children': children, #change this
        'infants': pens, #change this
    }




    url = "https://www.tallinn-airport.ee/wp-admin/admin-ajax.php"
    page = requests.post(url, data=payload)
    content = json.loads(page.text)
    ticket_link = content['data'].replace("\\", "")
    return ticket_link


def main():
    sihtkoht = input("Sisesta sistkoht: ").capitalize()
    kuupaev = input("Sisesta kuupaev: ")
    tagasi_lend = input("Sisesta tagasilend: ")
    adults = str(input("sisesta adults"))
    children = str(input("sisesta children"))
    pens = str(input("sisesta pens"))


    sihtkohad("forward", sihtkoht, kuupaev)

    print(get_tickets_link(sihtkoht, kuupaev, tagasi_lend, adults, children, pens))


# def get_best_ticket_prices():
#     s = requests.Session()
#     url = 'https://www.estravel.ee/lennupiletid/results/type/roundtrip/fromdate-0/2022-11-05/from-0/TLL/returndate/2022-11-11/to-0/AYT/adt/1/service/Economy'
#
#     r = s.get(url)
#     print(r)
#     r2 = s.post('https://www.estravel.ee/wp-json/flights/v1/flight-search?lang=et')
#     print(r2.content)
    # my_json = r.content.decode('utf8').replace("'", '"')
    # print(my_json)
    #
    # js = json.loads(my_json)
    #
    # for i in range(0, len(js["flights"]["flights"])):
    #     if js["flights"]["flights"][i]["isFastest"] == True:
    #         print(js["flights"]["flights"][i]["priceInfo"]["total"])
    #     if js["flights"]["flights"][i]["isOptimum"] == True:
    #         print(js["flights"]["flights"][i]["priceInfo"]["total"])
    #     if js["flights"]["flights"][i]["isCheapest"] == True:
    #         print(js["flights"]["flights"][i]["priceInfo"]["total"])



def get_best_ticket_prices(user_date, tagasilend, adults, children, infants, dest_airport_name, suund1):
    print(suund1)
    if suund1 == "forward":
        p = {"adt_count":adults,
            "chd_count":children,
            "inf_count":infants,
            "legs":[{"from":"TLL","to":dest_airport_name,"date":user_date}],
            "pref_carrier":'[]',
            "get_calendar":'true',
            "get_alternatives":'true',
            "service_class":"Economy"}
    elif suund1 == "back":
        p = {"adt_count":adults,
            "chd_count":children,
            "inf_count":infants,
            "legs":[{"from":dest_airport_name,"to":"TLL","date":user_date}],
            "pref_carrier":'[]',
            "get_calendar":'true',
            "get_alternatives":'true',
            "service_class":"Economy"}

    elif suund1 == "both":
        p = {"adt_count":adults,
            "chd_count":children,
            "inf_count":infants,
            "legs":[{"from":"TLL","to":dest_airport_name,"date":user_date},
            {"from":dest_airport_name,"to":"TLL","date":tagasilend}],
            "pref_carrier":'[]',
            "get_calendar":'true',
            "get_alternatives":'true',
            "service_class":"Economy"}

    else:
        p = ''
    print(p)
    r = requests.post('https://www.estravel.ee/wp-json/flights/v1/flight-search?lang=et', json=p)
    id = json.loads(r.text)
    id = json.dumps(id["result"]["search_id"])
    time.sleep(2)
    url = f"https://www.estravel.ee/wp-json/flights/v1/flight-results?lang=et&search_id={id}&calendar_id=false"
    js = requests.get(url)

    decode_js = js.content.decode('utf8').replace("'", '"')
    js = json.loads(decode_js)
    print(js)

    for i in range(0, len(js["flights"]["flights"])):
        if js["flights"]["flights"][i]["isFastest"] == True:
            print(js["flights"]["flights"][i]["priceInfo"]["total"])
        if js["flights"]["flights"][i]["isOptimum"] == True:
            print(js["flights"]["flights"][i]["priceInfo"]["total"])
        if js["flights"]["flights"][i]["isCheapest"] == True:
            print(js["flights"]["flights"][i]["priceInfo"]["total"])
    return js


    # pg = requests.get(url)
    # print(pg.text)
    # decode_js = pg.content.decode('utf8').replace("'", '"')
    # js = json.loads(decode_js)
    # print(js)


    # for i in range(0, len(js["flights"]["flights"])):
    #     if js["flights"]["flights"][i]["isFastest"] == True:
    #         print(js["flights"]["flights"][i]["priceInfo"]["total"])
    #     if js["flights"]["flights"][i]["isOptimum"] == True:
    #         print(js["flights"]["flights"][i]["priceInfo"]["total"])
    #     if js["flights"]["flights"][i]["isCheapest"] == True:
    #         print(js["flights"]["flights"][i]["priceInfo"]["total"])




#сделать словарь в котором будут эстонские и международные названия стран,
#чтобы при ввода страны первая функция могла находить нужное название на английскои
#и давть нужный инптут времени вылетов
#https://www.estravel.ee/wp-json/flights/v1/flight-results?lang=et&search_id=11776905&calendar_id=false

def kuupaev_kontroll(date):
    try:
        datetime.datetime.strptime(date, '%m.%d.%Y')
        result = True

    except ValueError:
        result = False

    return result






