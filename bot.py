from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
import os
from aiogram.dispatcher.filters import Text
from db_actions import bot_sales_find, delete_db, search_by_name
from app import main_app
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='5613441873:AAESCqAhksj0qLLlKPaPf61uLuCp1UO-2pg')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#функция для удаления файла со списком товаров
def delete_current_user(file_name):
    os.remove(f'{file_name}.txt')

#хендлер старт
@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Найти скидки', 'Поиск по названию' ,'Операции с БД']
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(*start_button)
    await message.answer("Товары со скидкой", reply_markup=keybord)

#класс состояния
class FSMInputName(StatesGroup):
    name = State()

#хендлер для перехода в меню поиска по названию
@dp.message_handler(Text(equals='Поиск по названию'))
async def search(message: types.Message):
    await message.answer("Введите название")
    await FSMInputName.name.set()

#хендлер для считатывания ответа, для поиска по нозванию
@dp.message_handler(state=FSMInputName.name)
async def state1(message: types.Message, state: FSMContext):
    product_name_answer = message.text
    await state.finish()
    print(product_name_answer)
    functionreturn = search_by_name(product_name_answer)
    message_text = ''
    if functionreturn != False:
        if len(functionreturn) > 10:
            for i, product in enumerate(functionreturn):
                if i == 10:
                    await message.answer(f'{message_text}', parse_mode='HTML')
                    message_text = ''
                elif i == 31:
                    break
                else:
                    message_text = message_text + f'ТОВАР: {product[0]}\n<a href ="{product[1]}">ССЫЛКА</a>\nСКИДКА: {product[2]}%\nСТАРАЯ ЦЕНА: {product[3]} руб.\nНОВАЯ ЦЕНА: {product[4]} руб.\n\n'
        elif len(functionreturn) == 0:
                message.answer('Товаров не найдено')
        else:
            for product in functionreturn:
                message_text = message_text + f'ТОВАР: {product[0]}\n<a href ="{product[1]}">ССЫЛКА</a>\nСКИДКА: {product[2]}%\nСТАРАЯ ЦЕНА: {product[3]} руб.\nНОВАЯ ЦЕНА: {product[4]} руб.\n\n'
            await message.answer(f'{message_text}', parse_mode='HTML')
        await message.answer('Полный список товаров в файле ниже')
        await message.reply_document(open(f'{product_name_answer}.txt', 'rb'))
    else:
        await message.answer('Нет товаров с таким названием, попробуй написать часть слово')
    delete_current_user(product_name_answer)


#хендлер для перехода в меню с операции БД
@dp.message_handler(Text(equals='Операции с БД'))
async def dbfunction(message: types.Message):
    db_button =['Обновить списки','Удалить всё из базы данных', 'Назад']
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(*db_button)
    await message.answer("Не нажимайте если не дурак", reply_markup=keybord)

#хэндлер для кнопки, переходящей в меню с выбором скидки
@dp.message_handler(Text(equals='Найти скидки'))
async def sales_menu(message: types.Message):
    sale_button = ['10-20%', '20-30%', '40-50%', '50-60%', '60-70%', '70-100%', 'Назад']
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(*sale_button)
    await message.answer("Товары со скидкой из Табрис", reply_markup=keybord)

#хэндлер для кнопки назад в меню
@dp.message_handler(Text(equals='Назад'))
async def start(message: types.Message):
    start_button = ['Найти скидки', 'Поиск по названию', 'Операции с БД']
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(*start_button)
    await message.answer("Товары со скидкой", reply_markup=keybord)

#хэндлер для кнопки очистки базы данных
@dp.message_handler(Text(equals='Удалить всё из базы данных'))
async def delete_message(message: types.Message):
    await message.answer('База удаляется')
    delete_db()
    await message.answer('База удалена!')

#хэндлер для кнопки обновить списки
@dp.message_handler(Text(equals='Обновить списки'))
async def refresh_db(message: types.Message):
    await message.answer('База данных обновляется')
    products_count = main_app()[0]
    await message.answer(f'База данных обновлена, добавлено {products_count} новых товаров.')

#функция для хэндлеров с поиском по размеру скидки
def search_by_nm(n, m):
    message_text = ''
    product_list = bot_sales_find(n,m)
    if product_list != 'Database error':
        for i, product in enumerate(product_list):
            striped_name = product[0][:-20]
            message_text = message_text + f'ТОВАР: {striped_name}\n<a href ="{product[1]}">ССЫЛКА</a>\nСКИДКА: {product[2]}%\nСТАРАЯ ЦЕНА: {product[3]} руб.\nНОВАЯ ЦЕНА: {product[4]} руб.\n\n'
            if i == 25:
                return message_text
            elif len(product_list) - 1 == i:
                return message_text
    else:
        return 'Ошибка с базой данных'

#хэндлеры для поиска по всем процентам скидки
@dp.message_handler(Text(equals='10-20%'))
async def discount_10_20(message: types.Message):
    await message.answer('Пожалуйста подождите')
    await message.answer(f'{search_by_nm(10,20)}', parse_mode='HTML')
    await message.answer('Полный список товаров в файле ниже')
    await message.reply_document(open(('от_10_до_20_скидки.txt'), 'rb'))
    delete_current_user('от_10_до_20_скидки')

@dp.message_handler(Text(equals='20-30%'))
async def discount_10_20(message: types.Message):
    await message.answer('Пожалуйста подождите')
    await message.answer(f'{search_by_nm(20, 30)}', parse_mode='HTML')
    await message.answer('Полный список товаров в файле ниже')
    await message.reply_document(open('от_20_до_30_скидки.txt', 'rb'))
    delete_current_user('от_20_до_30_скидки')

@dp.message_handler(Text(equals='30-40%'))
async def discount_10_20(message: types.Message):
    await message.answer('Пожалуйста подождите')
    await message.answer(f'{search_by_nm(30, 40)}', parse_mode='HTML')
    await message.answer('Полный список товаров в файле ниже')
    await message.reply_document(open('от_30_до_40_скидки.txt', 'rb'))
    delete_current_user('от_30_до_40_скидки')

@dp.message_handler(Text(equals='40-50%'))
async def discount_10_20(message: types.Message):
    await message.answer('Пожалуйста подождите')
    await message.answer(f'{search_by_nm(40, 50)}', parse_mode='HTML')
    await message.answer('Полный список товаров в файле ниже')
    await message.reply_document(open('от_40_до_50_скидки.txt', 'rb'))
    delete_current_user('от_40_до_50_скидки')

@dp.message_handler(Text(equals='50-60%'))
async def discount_10_20(message: types.Message):
    await message.answer('Пожалуйста подождите')
    await message.answer(f'{search_by_nm(50,60)}', parse_mode='HTML')
    await message.answer('Полный список товаров в файле ниже')
    await message.reply_document(open('от_50_до_60_скидки.txt', 'rb'))
    delete_current_user('от_50_до_60_скидки')

@dp.message_handler(Text(equals='60-70%'))
async def discount_10_20(message: types.Message):
    await message.answer('Пожалуйста подождите')
    await message.answer(f'{search_by_nm(60, 70)}', parse_mode='HTML')
    await message.answer('Полный список товаров в файле ниже')
    await message.reply_document(open('от_60_до_70_скидки.txt', 'rb'))
    delete_current_user('от_60_до_70_скидки')

@dp.message_handler(Text(equals='70-100%'))
async def discount_10_20(message: types.Message):
    await message.answer('Пожалуйста подождите')
    await message.answer(f'{search_by_nm(70, 100)}', parse_mode='HTML')
    await message.answer('Полный список товаров в файле ниже')
    await message.reply_document(open('от_70_до_100_скидки.txt', 'rb'))
    delete_current_user('от_70_до_100_скидки')

def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()