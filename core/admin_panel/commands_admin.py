from aiogram.fsm.context import FSMContext

from core.dispatcher import dp
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from core.settings import settings
from core.admin_panel.keyboard_admin import admin_keyboard, admin_send_answer  # Клавиатура для администратора
from core.FSM.FSM import FSMAnswer


@dp.message(Command('admin'))
async def cmd_admin(message: Message):
    if message.from_user.id == settings.bots.admin_id:
        await message.answer(
            "Админ панель",
            reply_markup=admin_keyboard,
        )


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@dp.message(StateFilter(FSMAnswer.message_from_admin))
async def process_fast_answer_on_question(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(text=message.text)
    await message.answer(
        text=f'<b>Проверьте ответ на вопрос</b>\n{message.text}',
        reply_markup=admin_send_answer
    )
