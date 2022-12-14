from telebot import types

delete_keyboard = types.ReplyKeyboardRemove()

direction_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
forward = types.KeyboardButton('Sinna')
back = types.KeyboardButton('Tagasi')
both = types.KeyboardButton('Mõlemad')

direction = direction_markup.add(forward, back, both)

link_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
jah = "Jah"
ei = "Ei"

link_vajalik = link_markup.add(jah, ei)



def kuupaevad_sinna(kuupaevad):
    kuupaead_sinna = []
    kuupaead_sinna_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for date in kuupaevad:
        button_sinna = types.KeyboardButton(date)
        kuupaead_sinna = kuupaead_sinna_markup.add(button_sinna)
    return kuupaead_sinna

def kuupaevad_tagasi(kuupaevad):
    kuupaead_tagasi = []
    kuupaead_tagasi_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for date in kuupaevad:
        button_tagasi = types.KeyboardButton(date)
        kuupaead_tagasi = kuupaead_tagasi_markup.add(button_tagasi)
    return kuupaead_tagasi


def countries(country_dict):
    countries = []
    countries_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for country in country_dict.keys():
        button_countries = types.KeyboardButton(country)
        countries = countries_markup.add(button_countries)
    return countries