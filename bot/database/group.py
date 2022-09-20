import sqlite3


class Group:
    def __init__(self, chat_id, classroom=None):
        self.chat_id = chat_id
        self.classroom = classroom

    @staticmethod
    def is_group_new(chat_id):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "SELECT * FROM groups WHERE chat_id = ?"
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
    async def get_all_groups():
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "SELECT * FROM groups"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            groups = []

            for record in result:
                groups.append(Group(chat_id=record[0]))

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                return groups

    async def write_to_db(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "INSERT INTO groups (chat_id) VALUES (?);"
            data = (self.chat_id,)
            cursor.execute(query, data)
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()

    async def add_classroom(self):
        try:
            sqlite_connection = sqlite3.connect("database.db")
            cursor = sqlite_connection.cursor()

            query = "UPDATE groups SET classroom = ? WHERE chat_id = ?;"
            data = (self.classroom, self.chat_id)
            cursor.execute(query, data)
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()

    async def remove_classroom(self):
        try:
            sqlite_connection = sqlite3.connect("database.db")
            cursor = sqlite_connection.cursor()

            query = "UPDATE groups SET classroom = NULL WHERE chat_id = ?;"
            data = (self.chat_id,)
            cursor.execute(query, data)
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()

    async def delete_group(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()

            query = "DELETE FROM groups WHERE chat_id = ?;"
            data = (self.chat_id,)
            cursor.execute(query, data)
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
