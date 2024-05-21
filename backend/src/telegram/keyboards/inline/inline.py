from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


# Кнопка, перенапрвляющая на регистрацию пользователя
def register_user() -> InlineKeyboardMarkup:
    signup_button = InlineKeyboardButton(text="Регистрация", callback_data="/signup")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[signup_button]])

    return keyboard


# Кнопка, перенапрвляющая на подбор питания
def pickup_food() -> InlineKeyboardMarkup:
    sport_food = InlineKeyboardButton(text="Подобрать спортивное питание", callback_data="/pickup")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[sport_food]])

    return keyboard


# Кнопки, выдающие список социальных сетей
def social_links() -> InlineKeyboardMarkup:
    tg_channel_link = 'https://t.me/healthy_body/'
    instagram_link = 'https://www.instagram.com/healthy_body/'

    tg_channel = InlineKeyboardButton(text="Наш Телеграм-канал", url=tg_channel_link)
    instagram = InlineKeyboardButton(text="Наш Instagram", url=instagram_link)

    markup = InlineKeyboardMarkup(inline_keyboard=[[tg_channel], [instagram],])

    return markup

def result() -> InlineKeyboardMarkup:
    url = 'https://google.com/'
    button = InlineKeyboardButton(text="Посмотреть результат", web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return markup