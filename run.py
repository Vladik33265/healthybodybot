from aiogram.filters import CommandStart, Command

from backend.src.db.db import engine, Base
from backend.src.telegram.bot import bot, dp
from backend.src.telegram.utils.commands.menu import set_main_menu
from backend.src.telegram.states import States

from backend.src.telegram.handlers.auth.start import start
from backend.src.telegram.handlers.auth.signup import signup, get_phone

from backend.src.telegram.handlers.pickup import (pickup_command, pickup_button, lets_pickup, main_target,
                                                  too_much_weight, trauma_team, cholesterol, hearth, lactose,
                                                  desire_skin, desire_fatigue, desire_immunity, desire_pain_muscles)

from backend.src.telegram.handlers.social import social
# from backend.src.telegram.handlers.support import support


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    # Регистрация кнопки меню в чате
    dp.startup.register(set_main_menu)

    # Регистрация обработчиков, связанных с командой /start
    dp.message.register(start, CommandStart())

    # Регистрация команды /signup
    dp.callback_query.register(signup, lambda c: c.data == '/signup')
    dp.message.register(get_phone, States.phone)

    # Регистрация обработчиков, связанных с командой /pickup
    dp.message.register(pickup_command, Command('pickup'))
    dp.callback_query.register(pickup_button, lambda c: c.data == '/pickup')
    dp.message.register(lets_pickup, States.confirm_pickup)
    dp.callback_query.register(main_target, lambda c: c.data.startswith('target'))
    dp.message.register(too_much_weight, States.overweight_state)
    dp.message.register(trauma_team, States.trauma_state)
    dp.message.register(cholesterol, States.cholesterol_state)
    dp.message.register(hearth, States.hearth_state)
    dp.message.register(lactose, States.lactose_state)
    dp.message.register(desire_skin, States.skin)
    dp.message.register(desire_fatigue, States.fatigue)
    dp.message.register(desire_immunity, States.immunity)
    dp.message.register(desire_pain_muscles, States.pain)

    # Регистрация обработчиков, связанных с командой /social
    dp.message.register(social, Command('social'))

    # Регистрация обработчиков, связанных с командой /support
    # dp.message.register(support, Command('support'))

    dp.run_polling(bot)
