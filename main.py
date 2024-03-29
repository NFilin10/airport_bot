import telebot
from config import token
import functionality
import keyboard
import os

#Link botile: https://t.me/airportTickets_bot
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Tere tulemast!\nSee on bot, mis aitab vaadata erinevaid lennureise ja pileteid\nAlustamiseks sisesta /otsi")


@bot.message_handler(commands=['otsi'])
def find(message):
    countries = functionality.get_country_indexes()
    bot.send_message(message.chat.id, f"Sisestage koht kuhu soovite minna: ", reply_markup=keyboard.countries(countries))
    bot.register_next_step_handler(message, get_place)


def get_place(message):
    user_place = message.text

    if user_place in functionality.get_country_indexes():
        bot.send_message(message.chat.id, "Valige suund:", reply_markup=keyboard.direction)
        bot.register_next_step_handler(message, get_suund, user_place)
    elif user_place == "/find":
        find(message)
    elif user_place == "/start":
        start()
    else:
        bot.send_message(message.chat.id, "Sellist kohta ei ole. Palun proovige uuesti")
        find(message)


def get_suund(message, sihtkoht):
    suund = message.text
    if suund == "Sinna":
        kuupaevad = functionality.get_avaliable_dates(sihtkoht)[0]
        bot.send_message(message.chat.id, "Valige kuupäev:", reply_markup=keyboard.kuupaevad_sinna(kuupaevad))
        bot.register_next_step_handler(message, date, suund, sihtkoht, None)
    elif suund == "Tagasi":
        kuupaevad = functionality.get_avaliable_dates(sihtkoht)[1]
        bot.send_message(message.chat.id, "Valige kuupäev:", reply_markup=keyboard.kuupaevad_tagasi(kuupaevad))
        bot.register_next_step_handler(message, date, suund, sihtkoht, None)
    elif suund == "Mõlemad":
        kuupaevad_sinna, kuupaevad_tagsi = functionality.get_avaliable_dates(sihtkoht)
        bot.send_message(message.chat.id, "Valige kuupäev:", reply_markup=keyboard.kuupaevad_sinna(kuupaevad_sinna))
        bot.register_next_step_handler(message, date, suund, sihtkoht, kuupaevad_tagsi)
    elif suund == "/find":
        find(message)
    elif suund == "/start":
        start()
    else:
        bot.send_message(message.chat.id, "Sellist suunda ei ole. Palun proovige uuesti")
        find(message)


def vale_kuupaev(message, sihtkoht, suund, kuupaevad_tagasi):
        bot.send_message(message.chat.id, "Valige kuupäev:")
        bot.register_next_step_handler(message, date, suund, sihtkoht, kuupaevad_tagasi)


def date(message, suund, sihtkoht, kuupaevad_tagsi):
    user_date = message.text
    if functionality.kuupaev_kontroll(user_date) == True:
        if suund == "Sinna":
            suund1 = "forward"
            lennud_sinna = functionality.sihtkohad('forward', sihtkoht, user_date)
            if lennud_sinna == "":
                bot.send_message(message.chat.id, "Sellel kuupäeval lendu ei toimu")
                find(message)
            else:
                bot.send_message(message.chat.id, f"On olemas järgmised lennud:\n\n{functionality.sihtkohad(suund1, sihtkoht, user_date)}")
                bot.send_message(message.chat.id, "Kas Te soovite piletite linki ja viivituse graafikut?", reply_markup=keyboard.link_vajalik)
                bot.register_next_step_handler(message, link_vajalik_vastus, sihtkoht, user_date, '1', None, suund1)
        elif suund == "Tagasi":
            suund1 = "back"
            lennud_tagasi = functionality.sihtkohad(suund1, sihtkoht, user_date)
            if lennud_tagasi == "":
                bot.send_message(message.chat.id, "Sellel kuupäeval lendu ei toimu")
                find(message)
            else:
                bot.send_message(message.chat.id, f"On olemas järgmised lennud:\n\n{lennud_tagasi}")
                bot.send_message(message.chat.id, "Kas Te soovite piletite linki ja viivituse graafikut?", reply_markup=keyboard.link_vajalik)
                bot.register_next_step_handler(message, link_vajalik_vastus, sihtkoht, user_date, '1', None, suund1)

        elif suund == "Mõlemad":
            suund1 = "both"
            lennud_sinna = functionality.sihtkohad('forward', sihtkoht, user_date)
            if lennud_sinna == "":
                bot.send_message(message.chat.id, "Sellel kuupäeval lendu ei toimu")
                find(message)
            else:
                bot.send_message(message.chat.id, f"On olemas järgmised lennud sinna:\n\n{lennud_sinna}")
                bot.send_message(message.chat.id, "Sisestage tagasilennu kuupäev:", reply_markup=keyboard.kuupaevad_tagasi(kuupaevad_tagsi))
                bot.register_next_step_handler(message, back_date, sihtkoht, suund, user_date, suund1, kuupaevad_tagsi)

    elif user_date == "/find":
        find(message)
    elif user_date == "/start":
        start()
    elif functionality.kuupaev_kontroll(user_date) == False:
        bot.send_message(message.chat.id, f"Kuupäev on sisestatud valesti. Palun proovige uuesti")
        vale_kuupaev(message, sihtkoht, suund, kuupaevad_tagsi)


def back_date(message, sihtkoht, suund, user_date, suund1, kuupaevad_tagasi):
    back_date = message.text
    if functionality.kuupaev_kontroll(back_date) == True:
        lennud_tagasi = functionality.sihtkohad("back", sihtkoht, back_date)
        if lennud_tagasi == "":
            bot.send_message(message.chat.id, "Sellel kuupäeval lendu ei toimu")
            find(message)
        else:
            bot.send_message(message.chat.id, f"On olemas järgmised lennud tagasi:\n\n{lennud_tagasi}")
            bot.send_message(message.chat.id, "Kas Te soovite piletite linki ja viivituse graafikut?", reply_markup=keyboard.link_vajalik)
            bot.register_next_step_handler(message, link_vajalik_vastus, sihtkoht, user_date, '0', back_date, suund1)
    elif back_date == "/find":
        find(message)
    elif back_date == "/start":
        start()
    elif functionality.kuupaev_kontroll(back_date) == False:
        bot.send_message(message.chat.id, f"Kuupäev on sisestatud valesti. Palun proovige uuesti")
        vale_kuupaev(message, sihtkoht, suund, kuupaevad_tagasi)


def link_vajalik_vastus(message, sihtkoht, user_date, suund, tagasilend, suund1):
    vastus = message.text
    sihtkoht = sihtkoht.replace("*", "")
    if vastus == "Ei":
        bot.send_message(message.chat.id, "Aitäh, et kasutasite boti!", reply_markup=keyboard.delete_keyboard)

    elif vastus == "/find":
        find(message)
    elif vastus == "/start":
        start()

    else:
        bot.send_message(message.chat.id, "Sisestage täiskasvanute arv:", reply_markup=keyboard.delete_keyboard)
        bot.register_next_step_handler(message, taiskasvanud, sihtkoht, user_date, suund, tagasilend, suund1)


def taiskasvanud(message, sihtkoht, user_date, suund, tagasilend, suund1):
    try:
        adults = int(message.text)
        bot.send_message(message.chat.id, "Sisestage laste arv:")
        bot.register_next_step_handler(message, lapsed, sihtkoht, user_date, suund, tagasilend, adults, suund1)
    except:
        bot.send_message(message.chat.id, "Vale sisend. Palun proovige uuesti")
        link_vajalik_vastus(message, sihtkoht, user_date, suund, tagasilend, suund1)


def lapsed(message, sihtkoht, user_date, suund, tagasilend, adults, suund1):
    try:
        children = int(message.text)
        bot.send_message(message.chat.id, "Sisestage imikute arv:")
        bot.register_next_step_handler(message, imikud, sihtkoht, user_date, suund, tagasilend, adults, children, suund1)
    except:
        bot.send_message(message.chat.id, "Vale sisend. Palun proovige uuesti")
        link_vajalik_vastus(message, sihtkoht, user_date, suund, tagasilend, suund1)


def imikud(message, sihtkoht, user_date, suund, tagasilend, adults, children, suund1):
    try:
        infants = int(message.text)
        bot.send_message(message.chat.id, f"See on Teie piletite link: {functionality.get_tickets_link(sihtkoht, user_date, suund, tagasilend, adults, children, infants, suund1)}")
        dest_airport_name = functionality.get_dest_airport_name(sihtkoht)
        l = list(dest_airport_name)
        dest_airport_name = ''.join(l[l.index('('):l.index(")")+1])

        bot.send_message(message.chat.id, "Laen alla parimad hinnad (20 sek)...")
        try:
            prices = functionality.get_best_ticket_prices(user_date, tagasilend, adults, children, infants, dest_airport_name, suund1)
            prices_msg = []

            for price in range(0, len(prices)):
                prices_msg.append(" ".join(prices[price]))

            formatted_prices = "\n".join(prices_msg)
            bot.send_message(message.chat.id, formatted_prices)
            send_graph(message, sihtkoht)
        except Exception:
            bot.send_message(message.chat.id, "Tekkis viga. Palun proovige uuesti")


    except Exception:
        bot.send_message(message.chat.id, "Vale sisend. Palun proovige uuesti")
        link_vajalik_vastus(message, sihtkoht, user_date, suund, tagasilend, suund1)


def send_graph(message, sihtkoht):
    all_dep, sihtkoht_dep = functionality.get_all_departures(sihtkoht)

    if sihtkoht_dep == {}:
        bot.send_message(message.chat.id, "Hetkel ei ole infot teie valitud sihtkoha kohta, seega on ainult teised sihtkohad")
    all_dep_viiv, all_dep_comp = functionality.time_difference_minutes(all_dep)
    sihtkoht_viiv, sihtkoht_comp = functionality.time_difference_minutes(sihtkoht_dep)
    if 0.0 in sihtkoht_viiv:
        sihtkoht_viiv = []
        sihtkoht_comp = []
    viivitus = functionality.graph(all_dep_viiv, all_dep_comp, sihtkoht_viiv, sihtkoht_comp)
    if os.path.exists('graph1.png'):
        if viivitus == 0.0:
            bot.send_message(message.chat.id, "Hetkel ei ole infot teie valitud sihtkoha kohta, seega on ainult teised sihtkohad")

        elif viivitus != []:
            bot.send_message(message.chat.id, f"Keskmine viivitus sihtkohta {sihtkoht} on {round(viivitus, 1)} minutit")

        photo = open('graph1.png', 'rb')
        bot.send_photo(message.chat.id, photo)
        os.remove('graph1.png')
    else:
        bot.send_message(message.chat.id, "Tekkis viga. Palun proovige uuesti")
        start(message)

if  __name__ == '__main__':
    bot.polling(none_stop=True)