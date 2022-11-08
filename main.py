import telebot
from config import token
import functionality
import keyboard


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Tere tulemast!\nSee on bot, mis aitab vaadata erinevaid lennureise ja pileteid\nAlustamiseks sisesta /find")


@bot.message_handler(commands=['find'])
def find(message):
    all_plases = []
    bot.send_message(message.chat.id, "Sisetage koht kuhu soovite minna")
    for place, id in functionality.get_country_indexes().items():
        all_plases.append(place)
    all_plases_formatted = '\n'.join(all_plases)
    bot.send_message(message.chat.id, f"Sisetage koht kuhu soovite minna:\n{all_plases_formatted}")
    bot.register_next_step_handler(message, get_place)


def get_place(message):
    user_place = message.text

    if user_place in functionality.get_country_indexes():
        bot.send_message(message.chat.id, "Valige suund", reply_markup=keyboard.direction)
        bot.register_next_step_handler(message, get_suund, user_place)
    else:
        bot.send_message(message.chat.id, "Sellist kohta ei ole. Palun proovige uuesti")
        find(message)


def get_suund(message, sihtkoht):
    suund = message.text
    print("suund:", suund)
    print("sihtkoht", sihtkoht)

    bot.send_message(message.chat.id, "Valige kuupäev (date.month.year)", reply_markup=keyboard.direction)
    bot.register_next_step_handler(message, date, suund, sihtkoht)


def vale_kuupaev(message, sihtkoht, suund):
        bot.send_message(message.chat.id, "Valige kuupäev (date.month.year)", reply_markup=keyboard.delete_keyboard)
        bot.register_next_step_handler(message, date, suund, sihtkoht)


def date(message, suund, sihtkoht):
    user_date = message.text
    print("date", user_date)
    if functionality.kuupaev_kontroll(user_date) == True:
        if suund == "Sinna":
            suund1 = "forward"
            bot.send_message(message.chat.id, f"On olemas järgmised lennud:\n\n{functionality.sihtkohad(suund, sihtkoht, user_date)}")
            bot.send_message(message.chat.id, "Kas Te soovite piletite linki ja viivituse?", reply_markup=keyboard.link_vajalik)
            bot.register_next_step_handler(message, link_vajalik_vastus, sihtkoht, user_date, '1', None, suund1)
        elif suund == "Tagasi":
            bot.send_message(message.chat.id, "Sisestage tagasi lennu kuupaev:")
            suund1 = "back"
            bot.send_message(message.chat.id, f"On olemas järgmised lennud:\n\n{functionality.sihtkohad(suund, sihtkoht, user_date)}")
            bot.send_message(message.chat.id, "Kas Te soovite piletite linki ja viivituse?", reply_markup=keyboard.link_vajalik)
            bot.register_next_step_handler(message, link_vajalik_vastus, sihtkoht, user_date, '1', None, suund1)

        elif suund == "Mõlemad":
            suund1 = "both"
            bot.send_message(message.chat.id, f"On olemas järgmised lennud sinna:\n\n{functionality.sihtkohad('forward', sihtkoht, user_date)}")
            bot.send_message(message.chat.id, "Sisestage tagasilennu kuupaev")
            bot.register_next_step_handler(message, back_date, sihtkoht, suund, user_date, suund1)

    else:
        bot.send_message(message.chat.id, f"Kuupäev on sisestatud valesti. Palun proovige uuesti")
        vale_kuupaev(message, sihtkoht, suund)


def back_date(message, sihtkoht, suund, user_date, suund1):
    back_date = message.text
    if functionality.kuupaev_kontroll(back_date) == True:
        bot.send_message(message.chat.id, f"On olemas järgmised lennud tagasi:\n\n{functionality.sihtkohad('back', sihtkoht, back_date)}")
        bot.send_message(message.chat.id, "Kas Te soovite piletite linki ja viivituse?", reply_markup=keyboard.link_vajalik)
        bot.register_next_step_handler(message, link_vajalik_vastus, sihtkoht, user_date, '0', back_date, suund1)
    else:
        bot.send_message(message.chat.id, f"Kuupäev on sisestatud valesti. Palun proovige uuesti")
        vale_kuupaev(message, sihtkoht, suund)


def link_vajalik_vastus(message, sihtkoht, user_date, suund, tagasilend, suund1):
    vastus = message.text
    if vastus == "Jah":
        bot.send_message(message.chat.id, "Sisestage taiskasvanute arv", reply_markup=keyboard.delete_keyboard)
        bot.register_next_step_handler(message, taiskasvanud, sihtkoht, user_date, suund, tagasilend, suund1)
    else:
        bot.send_message(message.chat.id, "Aitah, et kasutasite boti")


def taiskasvanud(message, sihtkoht, user_date, suund, tagasilend, suund1):
    adults = message.text
    bot.send_message(message.chat.id, "Siestage laste arv")
    bot.register_next_step_handler(message, lapsed, sihtkoht, user_date, suund, tagasilend, adults, suund1)


def lapsed(message, sihtkoht, user_date, suund, tagasilend, adults, suund1):
    children = message.text
    bot.send_message(message.chat.id, "Siestage imikute arv")
    bot.register_next_step_handler(message, imikud, sihtkoht, user_date, suund, tagasilend, adults, children, suund1)


def imikud(message, sihtkoht, user_date, suund, tagasilend, adults, children, suund1):
    infants = message.text
    bot.send_message(message.chat.id, f"See on Teie piletite link: {functionality.get_tickets_link(sihtkoht, user_date, suund, tagasilend, adults, children, infants, suund1)}")
    dest_airport_name = functionality.get_dest_airport_name(sihtkoht)
    dest_airport_name = dest_airport_name.replace("(", "").replace(")", "").split(' ')[1]

    bot.send_message(message.chat.id, "Laen alla parimad hinnad...")
    prices = functionality.get_best_ticket_prices(user_date, tagasilend, adults, children, infants, dest_airport_name, suund1)
    prices_msg = []
    for price in range(0, len(prices)):
        prices_msg.append(" ".join(prices[price]))

    formatted_prices = "\n".join(prices_msg)
    bot.send_message(message.chat.id, formatted_prices)


if  __name__ == '__main__':
    bot.polling(none_stop=True)