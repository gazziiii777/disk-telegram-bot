import random
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from core.dispatcher import dp, storage
from core.keyboards import start_keyboard, contact_the_admin_keyboard, main_menu_keyboard
from core.admin_panel.admin_commands import cmd_admin  # Подключение админ панели
from core.handlers.callback import main_menu, FSMContact  # Подключил callback`и


# Этот хэндлер будет срабатывать на команду /start вне состояний
@dp.message(Command("start"), StateFilter(default_state))
async def cmd_start(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAECxlllndCLYnENOYhrsQrmhxcx842mHgACJxYAAoJHGEhG_o_W8MthbjQE')
    await message.answer(
        "Приветсвенное сообщение",
        reply_markup=start_keyboard.keyboard,
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command('cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        "Приветсвенное сообщение",
        reply_markup=main_menu_keyboard.keyboard,
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@dp.message(StateFilter(FSMContact.message_for_admin))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(text=message.text)
    await message.answer(
        text=f'<b>Проверь свое письмо перед отправкой администратору:</b>\n{message.text}',
        reply_markup=contact_the_admin_keyboard.keyboard
    )


@dp.message()
async def send_echo(message: Message):
    await message.answer(
        text='Я даже представить себе не могу, '
             'что ты имеешь в виду :(\n\n'
             'Чтобы получить какую-нибудь шутку - '
             'отправь команду /joke'
    )
