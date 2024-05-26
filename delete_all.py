import sqlite3

def delete_all():
    try:
        database_path = 'healthy_body_db.db'
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        if conn:
            cursor.execute('''DELETE FROM users''')
            conn.commit()
        else:
            conn.rollback()
        print("deleted!!")
    except Exception as e:
        print("ERRORRRR:", e)


delete_all()