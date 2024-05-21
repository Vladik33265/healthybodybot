from aiogram.filters import CommandStart, Command

from backend.src.db.db import engine, Base
from backend.src.telegram.bot import bot, dp
from backend.src.telegram.utils.commands.menu import set_main_menu
from backend.src.telegram.states import States

from backend.src.telegram.handlers.auth.start import start
from backend.src.telegram.handlers.auth.signup import signup, get_phone
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
    ...

    # Регистрация обработчиков, связанных с командой /social
    dp.message.register(social, Command('social'))

    # Регистрация обработчиков, связанных с командой /support
    # dp.message.register(support, Command('support'))

    dp.run_polling(bot)
