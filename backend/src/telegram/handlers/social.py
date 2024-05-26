from aiogram.types import Message
from backend.src.telegram.keyboards.inline.inline import social_links
from backend.src.telegram.bot import logger

async def social(message: Message):
    try:
        markup = social_links()
        await message.answer('Хотите узнать лучше о нас?\n'
                             'Переходите по ссылкам на социальные сети ниже!', reply_markup=markup)
    except Exception as e:
        logger.exception("social", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
