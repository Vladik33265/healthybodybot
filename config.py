from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    db_name: str

@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tg_bot: TgBot
    db:     DatabaseConfig


env: Env = Env()
env.read_env()

config = Config(
    tg_bot = TgBot(
        token = env('TOKEN')
    ),
    db = DatabaseConfig(
        db_name = env('DB_NAME')
    ),
)

print(config.tg_bot.token)