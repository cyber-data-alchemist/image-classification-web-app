import sqlite3

def truncate_table():
    conn = sqlite3.connect('db/image_descriptions.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM descriptions')
    conn.commit()
    conn.close()

truncate_table()