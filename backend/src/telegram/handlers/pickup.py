from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from backend.src.db.models.models import Users

from backend.src.telegram.keyboards.reply.reply import to_pickup, yes_no
from backend.src.telegram.keyboards.inline.inline import register_user, result

from backend.src.telegram.keyboards.inline.pickup.inline import basic_target
from backend.src.telegram.keyboards.inline.pickup.product_dicts import product_dict

from backend.src.telegram.states import States
from backend.src.telegram.bot import logger, bot


async def pickup(user_id: int, state: FSMContext):
    try:
        user = Users.find_user(user_id)
        if user:
            await bot.send_message(user_id,
                                   "Хорошо! Чтобы подобрать подходящее спортивное питание и добавки, "
                                   "Вам необходимо ответить на несколько вопросов.\n"
                                   "\n"
                                   "Начнём?", reply_markup=to_pickup())
            await state.set_state(States.confirm_pickup)
        else:
            await bot.send_message(user_id,
                                   "Эта опция не доступна для тех, кто ещё не зарегистрировался в нашей системе.\n"
                                   "Для начала пройдите регистрацию, только потом Вы сможете "
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
            await message.answer("Какую основную цель Вы преследуете?",
                                 reply_markup=basic_target())
        if answer == 'Не сейчас':
            await message.answer("Хорошо, тогда Вы можете перейти в меню, и выбрать необходимую команду!")
    except Exception as e:
        logger.exception("lets pickup", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()


async def main_target(callback_query: CallbackQuery, state: FSMContext):
    try:
        user_data = await state.get_data()
        user_data['list'] = []

        data = callback_query.data.replace('target:', '')

        if data in product_dict:
            user_data['list'].append(product_dict[data])

        await bot.send_message(callback_query.from_user.id,
                               "Следующий вопрос.\n"
                               "Имеется ли у Вас <b>склонность к лишнему весу?</b>", reply_markup=yes_no())
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
                elif 'Жиросжигатели' in user_data['list']:
                    user_data['list'].append('Протеин')
                else:
                    user_data['list'].append('Протеин')
                    user_data['list'].append('Жиросжигатели')
            elif answer == 'Нет':
                pass
        if answer == message.text:
            await state.clear()

        await message.answer("Следующий вопрос.\n"
                             "Есть ли у Вас <b>травмы, боли в связках или суставах?</b>", reply_markup=yes_no())
        print("too_much_weight", user_data['list'])
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

        await message.answer("Есть ли у Вас <b>проблемы с высоким холестерином?</b>", reply_markup=yes_no())
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

        await message.answer("Присутствуют ли у Вас <b>заболевания сердца?</b>", reply_markup=yes_no())
        await state.set_state(States.hearth_state)
        await state.set_data(user_data)
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

        await message.answer("Имеется ли у Вас <b>непереносимость лактозы или животных белков?</b>",
                             reply_markup=yes_no())
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

        await message.answer("Может быть у Вас есть какие-то дополнительные пожелания по спортивному питанию?\n"
                             "\n"
                             "Например, <b>улучшить состояние кожи</b>?",
                             reply_markup=yes_no())

        await state.set_state(States.skin)
        await state.set_data(user_data)
    except Exception as e:
        logger.exception("lactose", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")

async def desire_skin(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()

        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if 'list' in user_data:
            if answer == 'Да':
                if 'Коллаген' not in user_data['list']:
                    user_data['list'].append('Коллаген')

        await message.answer("Хорошо, может быть Вы хотите <b>снизить утомляемость</b>?", reply_markup=yes_no())
        print("desire_skin", user_data['list'])
        await state.set_state(States.fatigue)
        await state.set_data(user_data)
    except Exception as e:
        logger.exception("desire_skin", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def desire_fatigue(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()

        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if 'list' in user_data:
            if answer == 'Да':
                if 'Бета-аланин' not in user_data['list']:
                    user_data['list'].append('Бета-аланин')

        await message.answer("Хотите ли Вы <b>укрепить иммунитет</b>?", reply_markup=yes_no())
        print("desire_fatigue", user_data['list'])
        await state.set_state(States.immunity)
        await state.set_data(user_data)
    except Exception as e:
        logger.exception("desire_fatigue", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def desire_immunity(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()

        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if 'list' in user_data:
            if answer == 'Да':
                if 'Поливитаминный комплекс' not in user_data['list']:
                    user_data['list'].append('Поливитаминный комплекс')

        await message.answer("<b>Снизить боль в мышцах?</b>", reply_markup=yes_no())

        await state.set_state(States.pain)
        await state.set_data(user_data)
    except Exception as e:
        logger.exception("desire_immunity", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def desire_pain_muscles(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()

        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if 'list' in user_data:
            if answer == 'Да':
                if 'BCAA' not in user_data['list']:
                    user_data['list'].append('BCAA')

        await bot.send_chat_action(message.from_user.id, 'typing')

        await message.answer("Я учёл все Ваши ответы на вопросы.\n"
                             "Вот наиболее подходящие для Вас добавки ниже по ссылке", reply_markup=result())
        await message.answer("Рекомендовано: "
                             "<b>проконсультироваться с врачом перед применением спортивного питания!!!</b>")
    except Exception as e:
        logger.exception("desire_immunity", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()
