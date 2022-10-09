from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

class Memory(StatesGroup):

    sale_value = State()
    product_name = State()
