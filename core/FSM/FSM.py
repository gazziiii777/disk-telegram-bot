# Cоздаем класс StatesGroup для нашей машины состояний
from aiogram.fsm.state import StatesGroup, State


class FSMContact(StatesGroup):
    message_for_admin = State()


class FSMAnswer(StatesGroup):
    message_from_admin = State()
