# ИНСТРУКЦИЯ

1. Создать проект
2. git clone https://github.com/Vladik33265/healthybodybot.git
3. Создать .venv
4. Активировать .venv
5. В консоли прописать pip install -r requirements.txt
6. Создать .env написать туда:
TOKEN=6660018566:AAE6ckPi7IWTtWIRasP_YZXGiuHqV1ig0zY
DB_NAME=healthy_body_db
7. Миграции:
1) alembic revision --autogenerate -m "Создать базу"
2) alembic upgrade head
8. запустить insert_pods.py
