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
            await message.answer("Добро пожаловать, я бот Sport Nutrition Assistant!\n"
                                 "Я смогу помочь Вам подобрать спортивное питание специально под Вас.\n"
                                 "Но я не знаю кто Вы, давайте сначала зарегистрируемся по кнопке ниже, "
                                 "и тогда мы сможем работать.", reply_markup=register_user())
    except Exception as e:
        logger.exception("start", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
