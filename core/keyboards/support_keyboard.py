from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons_1 = [
    [
        InlineKeyboardButton(text='Tехподдержка', callback_data='support')
    ],
    [
        InlineKeyboardButton(text='Назад', callback_data='main_menu')
    ],
]

# Создаем объекты инлайн-кнопок
buttons_2 = [
    [
        InlineKeyboardButton(text="Отправить", callback_data="send_the_support")
    ],
    [
        InlineKeyboardButton(text='Переписать', callback_data="support")
    ],
]

# Создаем объект инлайн-клавиатуры
support = InlineKeyboardMarkup(inline_keyboard=buttons_1)
question_to_support = InlineKeyboardMarkup(inline_keyboard=buttons_2)
