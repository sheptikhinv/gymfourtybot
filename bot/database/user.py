import sqlite3


class User:
    def __init__(self, chat_id, first_name, username=None, classroom_key=None):
        self.chat_id = chat_id
        self.first_name = first_name
        self.username = username
        self.classroom_key = classroom_key

    @staticmethod
    async def get_all_users():
        users = []
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "SELECT * FROM users;"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            for record in result:
                users.append(User(chat_id=record[0], first_name=record[1], username=record[2], classroom_key=record[3]))

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                return users

    @staticmethod
    def get_count_of_users():
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "SELECT count() FROM users;"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                return result[0]

    @staticmethod
    def is_user_new(chat_id):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "SELECT * FROM users WHERE chat_id = ?"
            data = (chat_id,)
            cursor.execute(query, data)
            record = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                if record is None:
                    return True
                else:
                    return False

    @staticmethod
    def get_user_by_id(chat_id):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "SELECT * FROM users WHERE chat_id = ?"
            data = (chat_id,)
            cursor.execute(query, data)
            record = cursor.fetchone()
            user = User(record[0], record[1], record[2], record[3])
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                return user
            return None

    async def delete_user(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "DELETE FROM users WHERE chat_id = ?"
            data = (self.chat_id,)
            cursor.execute(query, data)

            query = "DELETE FROM classrooms WHERE user_key = ?;"
            data = (self.classroom_key,)
            cursor.execute(query, data)

            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()

    async def write_to_db(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = """INSERT INTO users (chat_id, username, first_name, classroom_key) VALUES (?, ?, ?, ?);"""
            data = (self.chat_id, self.username, self.first_name, self.classroom_key)
            cursor.execute(query, data)
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()

    async def add_classroom(self, classroom):
        try:
            sqlite_connection = sqlite3.connect("database.db")
            cursor = sqlite_connection.cursor()

            query = "SELECT * FROM classrooms WHERE user_key = ? AND classroom = ?"
            data = (self.classroom_key, classroom)

            cursor.execute(query, data)
            if cursor.fetchone() is not None:
                return

            query = "INSERT INTO classrooms (user_key, classroom) VALUES (?, ?);"
            data = (self.classroom_key, classroom)
            cursor.execute(query, data)
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()

    async def remove_classroom(self, classroom=None):
        try:
            sqlite_connection = sqlite3.connect("database.db")
            cursor = sqlite_connection.cursor()

            if classroom is None:
                query = "DELETE FROM classrooms WHERE user_key = ?;"
                data = (self.classroom_key,)
                cursor.execute(query, data)
                sqlite_connection.commit()
                cursor.close()
            else:
                query = "DELETE FROM classrooms WHERE user_key = ? AND classroom = ?;"
                data = (self.classroom_key, classroom)
                cursor.execute(query, data)
                sqlite_connection.commit()
                cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def get_classrooms(self):
        try:
            sqlite_connection = sqlite3.connect("database.db")
            cursor = sqlite_connection.cursor()

            query = "SELECT classroom FROM classrooms WHERE user_key = ?"
            data = (self.classroom_key,)
            cursor.execute(query, data)
            result = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                return result
