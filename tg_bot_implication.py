import telebot
from telebot import types
from config import token
from main import get_country_indexes, sihtkohad, kuupaev_kontroll
import keyboard


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Tere tulemast!\nSee on bot, mis aitab vaadata erinevaid lennureise ja pileteid\nAlustamiseks sisesta /find")


@bot.message_handler(commands=['find'])
def find(message):
    all_plases = []
    bot.send_message(message.chat.id, "Sisetage koht kuhu soovite minna")
    for place, id in get_country_indexes().items():
        all_plases.append(place)
    all_plases_formatted = '\n'.join(all_plases)
    bot.send_message(message.chat.id, f"Sisetage koht kuhu soovite minna:\n{all_plases_formatted}")
    bot.register_next_step_handler(message, get_place)


def get_place(message):
    user_place = message.text

    if user_place in get_country_indexes():
        bot.send_message(message.chat.id, "Valige suund", reply_markup=keyboard.direction)
        bot.register_next_step_handler(message, get_suund, user_place)
    else:
        bot.send_message(message.chat.id, "Sellist kohta ei ole. Palun proovige uuesti", find(message))

def get_suund(message, sihtkoht):
    suund = message.text
    print("suund:", suund)
    print("sihtkoht", sihtkoht)

    bot.send_message(message.chat.id, "Valige kuupäev", reply_markup=keyboard.direction)
    bot.register_next_step_handler(message, date, suund, sihtkoht)


def vale_kuupaev(message, sihtkoht, suund):
        bot.send_message(message.chat.id, "Valige kuupäev", reply_markup=keyboard.direction)
        bot.register_next_step_handler(message, date, suund, sihtkoht)


def date(message, suund, sihtkoht):
    user_date = message.text
    print("date", user_date)
    if kuupaev_kontroll(user_date) == True:
        if suund == "Sinna":
            suund = "forward"
            bot.send_message(message.chat.id, f"On olemas järgmised lennud:\n\n{sihtkohad(suund, sihtkoht, user_date)}")
        elif suund == "Tagasi":
            suund = "back"
            bot.send_message(message.chat.id, f"On olemas järgmised lennud:\n\n{sihtkohad(suund, sihtkoht, user_date)}")
        elif suund == "Mõlemad":
            bot.send_message(message.chat.id, f"On olemas järgmised lennud sinna:\n\n{sihtkohad('forward', sihtkoht, user_date)}")
            bot.send_message(message.chat.id, f"On olemas järgmised lennud tagasi:\n\n{sihtkohad('back', sihtkoht, user_date)}")
    else:
        bot.send_message(message.chat.id, f"Kuupäev on sisestatud valesti. Palun proovige uuesti", vale_kuupaev(message, sihtkoht, suund))















if  __name__ == '__main__':
    bot.polling(none_stop=True)