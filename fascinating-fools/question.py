import sqlite3

db_path = 'storage/app.db'
connection = sqlite3.connect(db_path)
connection.row_factory = sqlite3.Row


class Question():
    def __init__(self, category):
        self.category = category
        self.connection = connection

    def get_questions(self):
        sql = 'SELECT * FROM question WHERE category = ?;'
        cursor = self.connection.cursor()
        cursor.execute(sql, (self.category, ))

        return [dict(row) for row in cursor.fetchall()]
