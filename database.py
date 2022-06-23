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
        self.user_database_name = config('USER_DATABASE_NAME')
        self.address_database_name = config('ADDRESS_DATABASE_NAME')
        self.order_database_name = config('ORDER_DATABASE_NAME')
        self.menu_database_name = config('MENU_DATABASE_NAME')


class BasicFunctions(EstablishConnection):
    def check_if_record_in_table(self, data_dict, table_name):
        sql_where_string = ' AND '.join([f"{x}='{data_dict[x]}'" for x in data_dict.keys()])
        self.cursor.execute(
                f"""
                SELECT * FROM {table_name}
                where {sql_where_string}
                """
            )
        return self.cursor.fetchall()


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
            f"""
            CREATE TABLE IF NOT EXISTS {self.user_database_name} (
                username TEXT NOT NULL,
                password bytea  NOT NULL,
                superuser boolean NOT NULL,
                PRIMARY KEY(username)
            )
            """
        )

    def address(self):
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.address_database_name} (
                address TEXT NOT NULL,
                address_line_2 TEXT,
                city TEXT NOT NULL,
                postal_code TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                username TEXT NOT NULL,
                FOREIGN KEY(username) REFERENCES {self.user_database_name}(username)
                ON DELETE CASCADE
            )
            """
        )

    def order(self):
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.order_database_name} (
                status TEXT NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                username TEXT NOT NULL,
                FOREIGN KEY(username) REFERENCES {self.user_database_name}(username)
                ON DELETE CASCADE
            )
            """
        )

    def menu(self):
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.menu_database_name} (
                title TEXT NOT NULL,
                description TEXT NOT NULL
            )
            """
        )


class Authorization(BasicFunctions):
    def register(self, data_dict):
        if self.check_if_record_in_table(data_dict, self.user_database_name):
            return {'error': 'User with that username already exists'}
        self.cursor.execute(
            f"""
            INSERT INTO {self.user_database_name}
            VALUES ('{data_dict['username']}', '{data_dict['password']}', false)
            """)
        self.cursor.close()
        self.conn.commit()

        return {'success': 'User successfully registered'}

    def login(self, data_dict):
        return bool(self.check_if_record_in_table(data_dict, self.user_database_name))

    def username_to_password(self, username):
        self.cursor.execute(
            f"""
            select username, password from {self.user_database_name}
            where username='{username}'
            """)
        return self.cursor.fetchall()


if __name__ == '__main__':
    CreateTables()
