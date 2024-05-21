from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import config


DATABASE_URL = f'sqlite:///{config.db.db_name}.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

class Base(DeclarativeBase):
    pass