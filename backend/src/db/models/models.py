from sqlalchemy import Column, Integer, String, Float, insert, select
from backend.src.db.db import Base, session


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False, unique=True)
    tg_username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)

    @classmethod
    def find_user(cls, tg_id: int):
        with session:
            is_user = select(cls).filter_by(tg_id=tg_id)
            result = session.execute(is_user)
            return result.scalar_one_or_none()

    @classmethod
    def create(cls, tg_id: int, tg_username: str, first_name: str, phone_number: str):
        with session:
            user = Users.find_user(tg_id)

            if not user:
                new_user = insert(cls).values(
                    tg_id = tg_id,
                    tg_username = tg_username,
                    first_name = first_name,
                    phone_number = phone_number
                )
                session.execute(new_user)
                session.commit()


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(String, nullable=False)

    @classmethod
    async def get_name(cls, name):
        with session:
            product = select(cls).filter_by(name=name)
            result = session.execute(product)
            return result.mappings().all()