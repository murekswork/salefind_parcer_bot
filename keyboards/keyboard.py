from aiogram import types

def menu_keyboard():
    buttons = ['Все скидки', 'Поиск по названию', 'Связь']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard

def empty_keyboard():
    keyboard = types.ReplyKeyboardRemove
    return keyboard

def sales_keyboard():
    buttons = ['20-40%', '40-60%', '60-80%', '80-100%']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

