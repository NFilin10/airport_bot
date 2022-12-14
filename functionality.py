import time
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import datetime
import numpy as np
import pylab

#Link botile: https://t.me/airportTickets_bot
def get_all_departures(sihtkoht):
    url = "https://www.tallinn-airport.ee/en/flight-info/realtime-flights/"
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

    sihtkoht_times = []
    all_departures_times = []

    for i in all_departures:
        if i == []:
            pass
        else:
            if sihtkoht == i[2] and i[4] != '' and i[4].split(" ")[0] != 'Arrived' and i[4] != 'Gate closed' and i[4].split(" ")[0] != 'Estimated' and i[4].split(" ")[0] != 'Boarding' and i[4].split(" ")[0] != 'Landed' and i[4].split(" ")[0] != 'Delayed' and i[4].split(" ")[0] != 'Departing' and i[4].split(" ")[0] != 'Cancelled':
                sihtkoht_times.append(i[0::4]+i[3:4])
            if sihtkoht != i[2] and i[4] != '' and i[4].split(" ")[0] != 'Arrived' and i[4] != 'Gate closed' and i[4].split(" ")[0] != 'Estimated' and i[4].split(" ")[0] != 'Boarding' and i[4].split(" ")[0] != 'Landed' and i[4].split(" ")[0] != 'Delayed' and i[4].split(" ")[0] != 'Departing' and i[4].split(" ")[0] != 'Cancelled':
                all_departures_times.append(i[0::4] + i[3:4])

    for i in sihtkoht_times:
        for j in range(1, 2):
            i[j] = i[j].replace("Departed ", "")

    for i in all_departures_times:
        for j in range(1, 2):
            i[j] = i[j].replace("Departed ", "")

    sihtkoht_times_dict = {}
    for i in range(len(sihtkoht_times)):

        if sihtkoht_times[i][2] not in sihtkoht_times_dict:

            sihtkoht_times_dict[sihtkoht_times[i][2]] = [sihtkoht_times[i][0:2]]
        else:
            sihtkoht_times_dict[sihtkoht_times[i][2]] += [sihtkoht_times[i][0:2]]

    all_departures_dict = {}
    for i in range(len(all_departures_times)):

        if all_departures_times[i][2] not in all_departures_dict:

            all_departures_dict[all_departures_times[i][2]] = [all_departures_times[i][0:2]]
        else:
            all_departures_dict[all_departures_times[i][2]] += [all_departures_times[i][0:2]]
    return all_departures_dict, sihtkoht_times_dict


def time_difference_minutes(d):
    format = '%H:%M'
    company = []
    viivitus = []
    sum = 0
    for k, v in d.items():
        for i in v:
            date1, date2  = i

            datetime1 = datetime.datetime.strptime(date1, format)
            datetime2 = datetime.datetime.strptime(date2, format)

            seconds = (datetime2 - datetime1).total_seconds()
            minutes = int(seconds / 60)
            if minutes <= 0:
                pass
            else:
                sum += minutes

        viivitus.append(round(sum/len(d[k]), 2))
        company.append(k)
        sum = 0
    return viivitus, company


def graph(all_viiv, all_comp, dest_viiv, dest_comp):
    pylab.clf()
    plt.title('Viivituse graafik', fontsize=12)
    plt.xlabel("Keskmine viivitus minutites", fontsize=9)

    plt.xticks(np.arange(0, max(all_viiv+dest_viiv)+1, 8))

    plt.tick_params(axis='y', labelsize=7, rotation=40)
    plt.tick_params(axis='x', labelsize=8, rotation=40)

    plt.hlines(all_comp, 0, all_viiv, linestyle="dashed")
    plt.hlines(dest_comp, 0, dest_viiv, linestyle="dashed", color='red')
    plt.xlim(0, None)
    plt.ylim(0, None)

    plt.scatter(all_viiv, all_comp, color='blue')
    plt.scatter(dest_viiv, dest_comp, color='red')
    plt.savefig('graph1.png')

    if dest_viiv != []:
        dest_viiv_kesk = 0
        for i in dest_viiv:
            dest_viiv_kesk += i
        dest_viiv_kesk = dest_viiv_kesk / len(dest_viiv)
        return dest_viiv_kesk
    else:
        return []


def get_country_indexes():
    url = 'https://www.tallinn-airport.ee/en/flight-info/destinations/'#"https://www.tallinn-airport.ee/lennuinfo/sihtkohad/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ids = soup.find_all('li', class_='destination-item')

    country_data = {}
    for id in ids:
        country_name = id.text.strip()
        country_id = id.get('data-destination')
        country_data[country_name] = country_id
    return country_data


def get_avaliable_dates(sihtkoht):
    payload = {
        'action': 'adm_get_destination_calendar_times',
        'id': get_country_indexes()[sihtkoht]
    }
    url = "https://www.tallinn-airport.ee/wp-admin/admin-ajax.php"

    page = requests.post(url, data=payload)

    content = page.text

    content_dict = json.loads(content)

    forward = content_dict['forward']
    back = content_dict['back']
    return forward, back


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
    if sihtkoht == "Sharm el Sheikh":
        airport = "Sharm El Sheikh, Ophira (SSH) - Egiptus"
        return airport
    else:
        url = 'https://www.tallinn-airport.ee/findflight.php?language=et&term=' + sihtkoht.capitalize()
        pg = requests.get(url)
        content = json.loads(pg.text)
        airport = content[0]["value"]

        return airport


def get_tickets_link(sihtkoht, kuupaev, suund, tagasi_lend, adults, children, pens, suund1):
    if suund1 == "back":
        payload = {
            'goToSearch': '1',
            'language': 'et',
            '_wpnonce': get_nonce(),
            '_wp_http_referer': '/lennuinfo/sihtkohad/',
            'action': 'search_flight_form_submit',
            'flightFrom': get_dest_airport_name(sihtkoht),
            'flightTo': 'Tallinn, Lennart Meri (TLL) - Eesti',
            'oneWay': suund,
            'startDate': kuupaev,
            'backDate': tagasi_lend,
            'adults': adults,
            'children': children,
            'infants': pens
        }

    else:
        payload = {
            'goToSearch': '1',
            'language': 'et',
            '_wpnonce': get_nonce(),
            '_wp_http_referer': '/lennuinfo/sihtkohad/',
            'action': 'search_flight_form_submit',
            'flightFrom': 'Tallinn, Lennart Meri (TLL) - Eesti',
            'flightTo': get_dest_airport_name(sihtkoht),
            'oneWay': suund,
            'startDate': kuupaev,
            'backDate': tagasi_lend,
            'adults': adults,
            'children': children,
            'infants': pens
        }

    url = "https://www.tallinn-airport.ee/wp-admin/admin-ajax.php"
    page = requests.post(url, data=payload)
    content = json.loads(page.text)
    ticket_link = content['data'].replace("\\", "")
    return ticket_link


def get_best_ticket_prices(user_date, tagasilend, adults, children, infants, dest_airport_name, suund1):
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

    r = requests.post('https://www.estravel.ee/wp-json/flights/v1/flight-search?lang=et', json=p)
    id = json.loads(r.text)

    search_id = json.dumps(id["result"]["search_id"])
    calendar_id = json.dumps(id["result"]["calendar_id"])

    time.sleep(20)

    p1 = {
        'lang':'et',
        'search_id':search_id,
        'calendar_id':calendar_id
    }

    url = f"https://www.estravel.ee/wp-json/flights/v1/flight-results?lang=et&search_id={search_id}&calendar_id={calendar_id}"
    js = requests.get(url, data=p1)
    decode_js = js.content.decode('utf8').replace("'", '"')
    js = json.loads(decode_js)

    prices = []

    for i in range(0, len(js["flights"]["flights"])):
        if js["flights"]["flights"][i]["isFastest"] == True:
            prices.append(["Kiireim", js["flights"]["flights"][i]["priceInfo"]["total"][0], "€"])
        if js["flights"]["flights"][i]["isOptimum"] == True:
            prices.append(["Parim", js["flights"]["flights"][i]["priceInfo"]["total"][0], "€"])
        if js["flights"]["flights"][i]["isCheapest"] == True:
            prices.append(["Soodsaim", js["flights"]["flights"][i]["priceInfo"]["total"][0], "€"])

    return prices


def kuupaev_kontroll(date):
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
        result = True

    except ValueError:
        result = False

    return result






