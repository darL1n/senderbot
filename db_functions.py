import sqlite3 as sql


def add_user(id, username, msg_id):
    with sql.connect('database.db') as db:
        cursor = db.cursor()
        params = (id, username, msg_id)
        cursor.execute("INSERT or IGNORE INTO users VALUES (?, ?, ?)", params)
        
        

def get_user_list():
    with sql.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users')


def add_sms(id, text):
    with sql.connect('database.db') as db:
        cursor = db.cursor()
        params = (id, text)
        cursor.execute("INSERT or IGNORE INTO messages VALUES (?, ?)", params)
        
def drop_table():
    with sql.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("""
            DROP TABLE  messages 
            """)
        


def update_value(msg, id):
    with sql.connect("database.db") as db:
        params = (msg, id)
        cursor = db.cursor()
        cursor.execute("UPDATE users SET MSG_ID=? WHERE id=?", params)