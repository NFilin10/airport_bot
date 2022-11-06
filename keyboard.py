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


