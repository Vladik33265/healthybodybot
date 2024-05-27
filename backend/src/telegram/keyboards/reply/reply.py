from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def to_pickup() -> ReplyKeyboardMarkup:
    yes = KeyboardButton(text="Начнём!")
    no = KeyboardButton(text="Не сейчас")
    kb = [[yes, no]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Вы готовы?",
        one_time_keyboard=True
    )
    return keyboard


def yes_no() -> ReplyKeyboardMarkup:
    yes = KeyboardButton(text="Да")
    no = KeyboardButton(text="Нет")

    kb = [[yes, no]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard