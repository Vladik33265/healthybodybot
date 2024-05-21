from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

product_names = []

def basic_target() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Набор мышц', callback_data='target:Набор мышц'),
            InlineKeyboardButton(text='Похудение', callback_data='target:Похудение')
        ],
        [
            InlineKeyboardButton(text='Увеличение силы', callback_data='target:Увеличение силы'),
            InlineKeyboardButton(text='Сушка', callback_data='target:Сушка')
        ],
        [
            InlineKeyboardButton(text='Набор общей массы', callback_data='target:Набор общей массы')
        ]
    ])
    return keyboard

def add_desire() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Улучшить состояние кожи', callback_data='desire:Улучшить состояние кожи')],
        [InlineKeyboardButton(text='Снизить утомляемость', callback_data='desire:Снизить утомляемость')],
        [InlineKeyboardButton(text='Укрепить иммунитет', callback_data='desire:Укрепить иммунитет')],
        [InlineKeyboardButton(text='Снизить боль в мышцах', callback_data='desire:Снизить боль в мышцах')]
    ])
    return keyboard