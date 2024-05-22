from aiogram.types import Message

from backend.src.telegram.keyboards.inline.inline import register_user, pickup_food
from backend.src.db.models.models import Users
from backend.src.telegram.bot import logger


async def start(message: Message):
    try:
        user = Users.find_user(message.from_user.id)

        if user:
            await message.answer("Привет! Рады, что ты вернулся к нам!\n"
                                 "Хочешь что-то снова подобрать себе? Нажимай на кнопку ниже!",
                                 reply_markup=pickup_food())
        else:
            await message.answer("Добро пожаловать, я Healthy Body Bot!\n"
                                 "Я смогу помочь тебе подобрать спортивное питание специально под тебя.\n"
                                 "Но я не знаю кто ты, давай сначала зарегистрируемся, и тогда мы сможем работать."
                                 "\n"
                                 "Давай зарегистрируем тебя по кнопке ниже", reply_markup=register_user())
    except Exception as e:
        logger.exception("start", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
