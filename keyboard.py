from telebot import types

markup = types.ReplyKeyboardMarkup()
forward = types.KeyboardButton('Sinna')
back = types.KeyboardButton('Tagasi')
both = types.KeyboardButton('Mõlemad')

direction =  markup.add(forward, back, both)


