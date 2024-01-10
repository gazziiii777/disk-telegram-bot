from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from core.dispatcher import dp, bot
from core.settings import settings
from core.keyboards import main_menu_keyboard, disk_keyboard, my_photo_and_video_keyboard
from core.db.questions.handlers_db import questions_add_db
from core.admin_panel.keyboard_admin import admin_answer
from core.admin_panel.callback_admin import not_now


@dp.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    # Высплывающее окошко
    await callback.answer(
        text="кайфарик марик тут типо тоже текст",
        show_alert=True
    )
    # После нажатия на кнопку текст меняется
    await callback.message.edit_text(
        text="типо главное меню",
        reply_markup=main_menu_keyboard.keyboard
    )


@dp.callback_query(F.data == "disk")
async def disk(callback: CallbackQuery):
    # После нажатия на кнопку текст меняется
    await callback.message.edit_text(
        text="ривет если ты хочешь написать письмо адмиину указать свою проблему",
        reply_markup=disk_keyboard.keyboard
    )


@dp.callback_query(F.data == "my_photo_and_video")
async def disk(callback: CallbackQuery):
    # После нажатия на кнопку текст меняется
    await callback.message.edit_text(
        text="ривет если ты хочешь написать письмо адмиину указать свою проблему",
        reply_markup=my_photo_and_video_keyboard.carousel
    )


# Cоздаем класс StatesGroup для нашей машины состояний
class FSMContact(StatesGroup):
    message_for_admin = State()


@dp.callback_query(F.data == "contact_the_admin")
async def contact_the_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Привет, тут ты можешь связаться с админом, для отмены напиши /cancel",
    )
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMContact.message_for_admin)


@dp.callback_query(F.data == "send_the_admin")
async def disk(callback: CallbackQuery, state: FSMContext):
    # После нажатия на кнопку текст меняется

    await questions_add_db(await state.get_data())

    await callback.message.edit_text(
        text="Ваше ссобщение отправленно",
        reply_markup=main_menu_keyboard.back
    )

    question = await state.get_data()
    if question.get('username') is not None and question.get('text') is not None:
        await bot.send_message(
            settings.bots.admin_id,
            text=f"<b>Username пользователя:</b> @{question.get('username')}\n<b>Вопрос от пользователя:</b>\n{question.get('text')}\n",
            reply_markup=admin_answer
        )
    await state.clear()
