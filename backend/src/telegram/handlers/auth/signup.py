from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from backend.src.telegram.bot import bot, logger
from backend.src.telegram.states import States
from backend.src.telegram.keyboards.inline.inline import pickup_food
from backend.src.db.models.models import Users


async def signup(callback_query: CallbackQuery, state: FSMContext):
    try:
        user = Users.find_user(callback_query.from_user.id)

        if user:
            await bot.send_message(callback_query.from_user.id,
                                   f"{callback_query.from_user.first_name}, ты зарегистрирован у нас!\n"
                                   "Тебе доступны мои инструменты, взгляни на меню.")
        else:
            await bot.send_message(callback_query.from_user.id,
                                   "Регистрация займёт менее 1 одном минуты. "
                                   "После неё ты сможешь продолжить работу со мной!.\n"
                                   "Напиши свой номер телефона..")
            await state.set_state(States.phone)
    except Exception as e:
        logger.exception("signup", e)
        await bot.send_message(callback_query.from_user.id,
                               "Кажется, произошла какая-то ошибка.\n"
                               "Стараемся разобраться с этим, извините за неудобства...")


async def get_phone(message: Message, state: FSMContext):
    try:
        await state.update_data(phone=message.text)
        get_data = await state.get_data()
        phone = get_data.get('phone')

        Users.create(tg_id=message.from_user.id,
                     tg_username=message.from_user.username,
                     first_name=message.from_user.first_name,
                     phone_number=phone)
        await message.answer(f"Отлично, {message.from_user.first_name}! Теперь мы можем начинать работу.\n"
                             "Если ты хочешь, чтобы я подобрал для тебя спортивное питание, "
                             "тогда переходи по кнопке ниже", reply_markup=pickup_food())
    except Exception as e:
        logger.exception("get_phone", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()