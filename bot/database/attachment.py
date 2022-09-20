import sqlite3


class Attachment:
    def __init__(self, name, id, date):
        self.name = name
        self.id = id
        self.date = date

    @staticmethod
    def get_latest_attachment():
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "SELECT * FROM timetable ORDER BY ID DESC LIMIT 1;"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                return result[0]

    def create_new(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            if self.is_new():
                query = """INSERT INTO timetable (name, id, date) VALUES (?, ?, ?);"""
                data = (self.name, self.id, self.date)
                cursor.execute(query, data)
                sqlite_connection.commit()
                cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def is_new(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = """SELECT * FROM timetable WHERE id = ?;"""
            cursor.execute(query, (self.id,))
            result = cursor.fetchone()
            if result is not None:
                return False
            else:
                return True

        except sqlite3.Error as error:
            print(error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()