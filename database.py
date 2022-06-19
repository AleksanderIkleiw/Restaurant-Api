import psycopg2
from decouple import config


class EstablishConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=config('HOST_NAME'),
            database=config('DATABASE_NAME'),
            user=config('USER_NAME'),
            password=config('PASSWORD'),
            port=config('PORT', cast=int)
        )
        self.cursor = self.conn.cursor()


class CreateTables(EstablishConnection):
    def __init__(self):
        super().__init__()

        self.user()
        self.address()
        self.order()
        self.menu()

        self.cursor.close()
        self.conn.commit()

    def user(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS restaurant_user (
                username TEXT NOT NULL,
                password bytea  NOT NULL,
                PRIMARY KEY(username)
            )
            """
        )

    def address(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS address (
                address TEXT NOT NULL,
                address_line_2 TEXT,
                city TEXT NOT NULL,
                postal_code TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                username TEXT NOT NULL,
                FOREIGN KEY(username) REFERENCES restaurant_user(username)
                ON DELETE CASCADE
            )
            """
        )

    def order(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS restaurant_order (
                status TEXT NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                username TEXT NOT NULL,
                FOREIGN KEY(username) REFERENCES restaurant_user(username)
                ON DELETE CASCADE
            )
            """
        )

    def menu(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS menu (
                title TEXT NOT NULL,
                description TEXT NOT NULL
            )
            """
        )


if __name__ == '__main__':
    CreateTables()