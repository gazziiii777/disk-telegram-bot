from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.dispatcher import dp, bot
from core.db.questions.functions_db import delete_question_from_db
from core.FSM.FSM import FSMAnswer

question_info = dict()


async def question_info_for_answer(question):
    global question_info
    question_info = question


@dp.callback_query(F.data == "not_now")
async def not_now(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()


@dp.callback_query(F.data == "delete_question")
async def delete_question(callback: CallbackQuery):
    await delete_question_from_db(question_info)
    await callback.answer()
    await callback.message.delete()


@dp.callback_query(F.data == "answer_now")
async def answer_now(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f"ответ на вопрос: <b>Username пользователя:</b> @{question_info.get('username')}\n<b>Вопрос от пользователя:</b>\n{question_info.get('text')}\n",
    )
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMAnswer.message_from_admin)


@dp.callback_query(F.data == "send_answer")
async def disk(callback: CallbackQuery, state: FSMContext):
    # После нажатия на кнопку текст меняется
    await callback.message.delete()
    await delete_question_from_db(question_info)
    await callback.answer(
        text="Ваша сообщение отпраленно",
        show_alert=True,
    )
    question = await state.get_data()
    await bot.send_message(
        question_info.get("id"),
        text=f"<b>Ответ от администратора</b>\n{question.get('text')}",
    )
    await state.clear()
