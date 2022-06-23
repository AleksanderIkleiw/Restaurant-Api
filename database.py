import psycopg2
from decouple import config
from enum import Enum


class DatabaseManager:
    def __enter__(self):
        self.conn = psycopg2.connect(
            host=config('HOST_NAME'),
            database=config('DATABASE_NAME'),
            user=config('USER_NAME'),
            password=config('PASSWORD'),
            port=config('PORT', cast=int)
        )
        self.conn.autocommit = True
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class Constants(Enum):
    user_database_name = config('USER_DATABASE_NAME')
    address_database_name = config('ADDRESS_DATABASE_NAME')
    order_database_name = config('ORDER_DATABASE_NAME')
    menu_database_name = config('MENU_DATABASE_NAME')


def get_menu():
    with DatabaseManager() as cursor_:
        cursor_.execute(
            f"""
            SELECT * FROM {Constants.menu_database_name}
            """)
        return cursor_.fetchall()


def check_if_record_in_table(data_dict, table_name):
    sql_where_string = ' AND '.join([f"{x}='{data_dict[x]}'" for x in data_dict.keys()])
    with DatabaseManager() as cursor_:
        cursor_.execute(
                f"""
                SELECT * FROM {table_name}
                where {sql_where_string}
                """
            )
        return cursor_.fetchall()


class BasicFunctions:
    pass


def user(cursor_):
    cursor_.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {Constants.user_database_name.value} (
            username TEXT NOT NULL,
            password bytea  NOT NULL,
            superuser boolean NOT NULL,
            PRIMARY KEY(username)
        )
        """
    )


def address(cursor_):
    cursor_.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {Constants.address_database_name.value} (
            address TEXT NOT NULL,
            address_line_2 TEXT,
            city TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            username TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES {Constants.user_database_name.value}(username)
            ON DELETE CASCADE
        )
        """
    )


def order(cursor_):
    cursor_.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {Constants.order_database_name.value} (
            status TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            username TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES {Constants.user_database_name.value}(username)
            ON DELETE CASCADE
        )
        """
    )


def menu(cursor_):
    cursor_.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {Constants.menu_database_name.value} (
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
        """
    )


def username_to_password(username):
    with DatabaseManager() as cursor_:
        cursor_.execute(
            f"""
            select username, password from {Constants.user_database_name.value}
            where username='{username}'
            """)
        return cursor_.fetchall()


def register(data_dict):
    if check_if_record_in_table(data_dict, Constants.user_database_name.value):
        return {'error': 'User with that username already exists'}
    with DatabaseManager() as cursor_:
        cursor_.execute(
            f"""
            INSERT INTO {Constants.user_database_name.value}
            VALUES ('{data_dict['username']}', '{data_dict['password']}', false)
            """)

    return {'success': 'User successfully registered'}


def login(data_dict):
    return bool(check_if_record_in_table(data_dict, Constants.user_database_name.value))


if __name__ == '__main__':
    with DatabaseManager() as cursor:
        user(cursor)
        address(cursor)
        order(cursor)
        menu(cursor)
