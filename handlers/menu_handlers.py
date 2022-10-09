from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from . import dp
from keyboards.keyboard import menu_keyboard, sales_keyboard
from controller import find_by_name_controller, parse_admin_func, find_by_sale_value_controller
from FSM import Memory


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Добро пожаловать в меню', reply_markup=menu_keyboard())


@dp.message_handler(Text(equals='Все скидки'))
async def all_sales(message: types.Message):
    await message.answer('введи процент скидки например 20 30 или 20-30', reply_markup=sales_keyboard())
    await Memory.sale_value.set()


@dp.message_handler(state=Memory.sale_value)
async def fsm_get_sale_value(message: types.Message, state: FSMContext):
    await find_by_sale_value_controller(message.text, message.from_user.id)
    await message.answer('поиск закончен', reply_markup=menu_keyboard())
    await state.finish()


@dp.message_handler(Text(equals='Поиск по названию'))
async def find_by_name_handler(message: types.Message):
    await message.answer('давай название товара')
    await Memory.product_name.set()


@dp.message_handler(state=Memory.product_name)
async def fsm_get_name(message: types.Message, state: FSMContext):
    await state.finish()
    await find_by_name_controller(message.text, message.from_user.id)
    await message.answer('во че я найти смог', reply_markup=menu_keyboard())


@dp.message_handler(Text(equals='подгрузи заново бро'))
async def admin_command_parse(message: types.Message):
    await message.answer('тогда ничего не трогай пока!')
    await parse_admin_func(message.from_user.id)
    await message.answer('ну все)', reply_markup=menu_keyboard())


@dp.message_handler(Text(equals='Связь'))
async def menu_contact(message: types.Message):
    await message.answer('Единственный контакт разработчика @livinlegen', reply_markup=menu_keyboard())
