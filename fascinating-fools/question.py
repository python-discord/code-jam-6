import sqlite3


class Question():
    db_path = 'storage/app.db'

    def __init__(self, category):
        self.category = category
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    def get_questions(self):
        sql = 'SELECT * FROM question WHERE category = ?;'
        cursor = self.connection.cursor()
        cursor.execute(sql, (self.category, ))

        return [dict(row) for row in cursor.fetchall()]
