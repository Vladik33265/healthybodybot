from aiogram import Bot
from aiogram.types import BotCommand

from backend.src.telegram.utils.commands.command_list import commands
from config import config

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


# Кнопка меню, которая упаравляет основным функционалом
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in commands.items()
    ]
    await bot.set_my_commands(main_menu_commands)