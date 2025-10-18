from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class ArizaState(StatesGroup):
    chat_id = State()
    ism = State()
    familiya = State()
    telefon_raqam = State()
    ariza = State()
    text = State()
    tasdiqlash = State()
    