from docx import Document
import pandas as pd
import sqlite3

# Чтение Word-файла
doc = Document('таблица.docx')

# Извлечение таблицы из Word-файла
table = doc.tables[0]

# Преобразование таблицы в DataFrame
data = [[cell.text for cell in row.cells] for row in table.rows]
df = pd.DataFrame(data)

df.columns = ['id', 'name', 'brand', 'description', 'price', 'count']

# Установка соединения с базой данных SQLite3
conn = sqlite3.connect('healthy_body_db.db')

# Запись данных из DataFrame в базу данных SQLite3
df.to_sql('products', conn, if_exists='replace', index=False)
