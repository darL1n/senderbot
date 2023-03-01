import sqlite3 as sql
import os


def create_db():
    with sql.connect('database.db', check_same_thread=False) as db:
        curs = db.cursor()
        
        db.commit()
        # создание таблицы users
        curs.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER NOT NULL PRIMARY KEY ,
                        username TEXT, msg_id INTEGER
                        )
                    """)
        db.commit()
        # создание таблицы messages
        curs.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER NOT NULL PRIMARY KEY,
                body TEXT)
            """)
        db.commit()

    




























# import sqlite3

# class DBHelper: 
#     def __init__(self, dbname="bot.sqlite3"):
#         self.dbname = dbname    
#         self.conn = sqlite3.connect(dbname)


    
#     def setup(self):
#         stmt = "CREATE TABLE IF NOT EXISTS items ()"
#         self.conn.execute(stmt)
#         self.conn.commit()

#     def add_item(self, item_text):
#         stmt = "INSERT INTO items (description) VALUES (?)"
#         args = (item_text, )
#         self.conn.execute(stmt, args)
#         self.conn.commit()

#     def delete_item(self, item_text):
#         stmt = "DELETE FROM items WHERE description = (?)"
#         args = (item_text, )
#         self.conn.execute(stmt, args)
#         self.conn.commit()

#     def get_items(self):
#         stmt = "SELECT description FROM items"
#         return [x[0] for x in self.conn.execute(stmt)]