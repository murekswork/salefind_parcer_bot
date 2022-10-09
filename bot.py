from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
import os
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import MAIN_TOKEN
from keyboards.keyboard import menu_keyboard
from FSM import storage


bot = Bot(token=MAIN_TOKEN)

dp = Dispatcher(bot, storage=storage)


