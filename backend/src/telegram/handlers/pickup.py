from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from backend.src.db.models.models import Users

from backend.src.telegram.keyboards.reply.reply import to_pickup, yes_no
from backend.src.telegram.keyboards.inline.inline import register_user, result

from backend.src.telegram.keyboards.inline.pickup.inline import basic_target, add_desire
from backend.src.telegram.keyboards.inline.pickup.product_dicts import product_dict

from backend.src.telegram.states import States
from backend.src.telegram.bot import logger, bot


async def pickup(user_id: int, state: FSMContext):
    try:
        user = Users.find_user(user_id)
        if user:
            await bot.send_message(user_id,
                                   "Хорошо! Но перед тем, как мы подобрать тебе спортивное питание, "
                                   "у меня есть несколько вопросов, касающихся твоего физического здоровья.\n"
                                   "Начнём?", reply_markup=to_pickup())
            await state.set_state(States.confirm_pickup)
        else:
            await bot.send_message(user_id,
                                   "Эта опция не доступна для тех, кто ещё не зарегистрировался в нашей системе.\n"
                                   "Для начала пройди регистрацию, только потом ты сможешь "
                                   "пользоваться моими инструментами", reply_markup=register_user())
    except Exception as e:
        logger.exception("pickup", e)

async def pickup_command(message: Message, state: FSMContext):
    await pickup(message.from_user.id, state)

async def pickup_button(callback_query: CallbackQuery, state: FSMContext):
    await pickup(callback_query.from_user.id, state)

async def lets_pickup(message: Message, state: FSMContext):
    try:
        await state.update_data(answer=message.text)
        get_answer = await state.get_data()
        answer = get_answer.get('answer')

        if answer == 'Начнём!':
            await message.answer("Итак.. первый вопрос:\n"
                                 "Какова твоя основная цель подбора спортивного питания?",
                                 reply_markup=basic_target())
        if answer == 'Не сейчас':
            await message.answer("Хорошо, тогда ты можешь перейти в меню, и выбрать необходимую команду!")
    except Exception as e:
        logger.exception("lets pickup", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def main_target(callback_query: CallbackQuery, state: FSMContext):
    try:
        user_data = await state.get_data()
        user_data['list'] = []

        data = callback_query.data.replace('target:', '')

        if data in product_dict:
            user_data['list'].append(product_dict[data])

        await bot.send_message(callback_query.from_user.id,
                               "Следующий вопрос.\n"
                               "Имеется ли у тебя склонность к лишнему весу?", reply_markup=yes_no())
        await state.set_state(States.overweight_state)
        await state.set_data(user_data)
    except Exception as e:
        logger.exception("main_target", e)
        await bot.send_message(callback_query.from_user.id,
                               "Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def too_much_weight(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()

        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if 'list' in user_data:
            if answer == 'Да':
                if 'Протеин' in user_data['list']:
                    user_data['list'].append('Жиросжигатели')
                if 'Жиросжигатели' in user_data['list']:
                    user_data['list'].append('Протеин')
                else:
                    user_data['list'].append('Протеин')
                    user_data['list'].append('Жиросжигатели')

        await message.answer("Следующий вопрос.\n"
                             "Есть ли у тебя травмы, боли в связках или суставах?", reply_markup=yes_no())
        await state.set_state(States.trauma_state)
        await state.set_data(user_data)
    except Exception as e:
        logger.exception("too_much_weight", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def trauma_team(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()

        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if 'list' in user_data:
            if answer == 'Да':
                user_data['list'].append('Глюкозамин/хондроитин')

        await message.answer("Окей, следующий вопрос. Почти закончили..\n"
                             "Есть ли у тебя проблемы с высоким холестерином?", reply_markup=yes_no())
        await state.set_state(States.cholesterol_state)
        await state.set_data(user_data)
    except Exception as e:
        logger.exception("lets pickup", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def cholesterol(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()

        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if 'list' in user_data:
            if answer == 'Да':
                user_data['list'].append('Омега 3-6-9')

        await message.answer("Окей, следующий вопрос. Почти закончили..\n"
                             "Присутствуют ли у тебя заболевания сердца?", reply_markup=yes_no())
        await state.set_state(States.hearth_state)
        await state.set_data(user_data)
        await message.answer("P.S От врачей:\n"
                             "Настоятельно рекомендуется не использовать добавки, "
                             "содержащие кофеин и другие стимуляторы")
    except Exception as e:
        logger.exception("trauma_team", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def hearth(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()

        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if 'list' in user_data:
            if answer == 'Да':
                user_data['list'].append('Поливитаминный комплекс')

        await message.answer("Имеется ли у Вас непереносимость лактозы или животных белков??", reply_markup=yes_no())
        await state.set_state(States.lactose_state)
        await state.set_data(user_data)
    except Exception as e:
        logger.exception("hearth", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def lactose(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()

        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if 'list' in user_data:
            if answer == 'Да':
                for i in user_data['list']:
                    if i == 'Протеин':
                        user_data['list'].remove('Протеин')
                    if i == 'Гейнер':
                        user_data['list'].remove('Гейнер')

                user_data['list'].append('Соевый изолят')

        await message.answer("Может быть у Вас есть какие-то дополнительные пожелания по спортивному питанию?",
                             reply_markup=add_desire())
        await state.set_data(user_data)
    except Exception as e:
        logger.exception("lactose", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def additional_desire(callback_query: CallbackQuery, state: FSMContext):
    try:
        user_data = await state.get_data()
        data = callback_query.data.replace('desire:', '')

        if 'list' in user_data:
            if data == 'Улучшить состояние кожи':
                user_data['list'].append('Коллаген')
            if data == 'Снизить утомляемость':
                user_data['list'].append('Бета-аланин')
            if data == 'Укрепить иммунитет':
                if 'Поливитаминный комплекс' not in user_data['list']:
                    user_data['list'].append('Поливитаминный комплекс')
            if data == 'Снизить боль в мышцах':
                user_data['list'].append('BCAA')
            await state.set_data(user_data)
            print(user_data['list'])

        await bot.send_chat_action(callback_query.from_user.id, action='typing')
        # await bot.send_message(callback_query.from_user.id,
        #                        "Спасибо большое, что ответили на все вопросы и дошли до конца!\n"
        #                        "Я подобрал для Вас наиболее подходящее спортивное питание, Вы можете посмотреть ниже",
        #                        reply_markup=result())
        list_str = "\n".join(user_data['list'])

        await bot.send_message(callback_query.from_user.id,
                               "Наиболее подходящие для вас добавки:\n"
                               f"{list_str}")
    except Exception as e:
        logger.exception("additional_desire", e)
        await bot.send_message(callback_query.from_user.id,
                               "Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
