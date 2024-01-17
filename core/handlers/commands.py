import random
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from core.dispatcher import dp
from core.keyboards import start_keyboard, support_keyboard, main_menu_keyboard
from core.handlers.callback import FSMContact  # Подключил callback`и


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
async def cmd_cancel(message: Message, state: FSMContext):
    await message.answer(
        "Приветсвенное сообщение",
        reply_markup=main_menu_keyboard.keyboard,
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@dp.message(StateFilter(FSMContact.message_for_admin))
async def process_question_to_support(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(id=message.from_user.id, text=message.text, username=message.from_user.username,
                            answer=False)
    await message.answer(
        text=f'<b>Пожалуйста, проверьте свое письмо перед отправкой в техподдержку:</b>\n{message.text}',
        reply_markup=support_keyboard.question_to_support
    )


@dp.message()
async def send_echo(message: Message):
    await message.answer(
        text='Я даже представить себе не могу, '
             'что ты имеешь в виду :(\n\n'
             'Чтобы получить какую-нибудь шутку - '
             'отправь команду /joke'
    )
