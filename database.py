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
            SELECT * FROM {Constants.menu_database_name.value}
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


def create_user_table(cursor_):
    cursor_.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {Constants.user_database_name.value} (
            username TEXT NOT NULL UNIQUE,
            password bytea  NOT NULL,
            superuser boolean NOT NULL,
            PRIMARY KEY(username)
        )
        """
    )


def create_address_table(cursor_):
    cursor_.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {Constants.address_database_name.value} (
            address TEXT NOT NULL,
            address_line_2 TEXT,
            city TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            surname TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES {Constants.user_database_name.value}(username) ON DELETE CASCADE
        )
        """
    )


def create_order_table(cursor_):
    cursor_.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {Constants.order_database_name.value} (
            status TEXT NOT NULL,
            username TEXT NOT NULL,
            item_ids integer[] NOT NULL,
            order_id TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES {Constants.user_database_name.value}(username) ON DELETE CASCADE,
            FOREIGN KEY(username) REFERENCES {Constants.address_database_name.value}(username) ON DELETE CASCADE
        )
        """
    )


def create_menu_table(cursor_):
    cursor_.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {Constants.menu_database_name.value} (
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price FLOAT NOT NULL,
            id INT NOT NULL
        )
        """
    )


def get_user_address(username):
    with DatabaseManager() as cursor_:
        cursor_.execute(
            f"""
            SELECT * from {Constants.address_database_name.value}
            where username = '{username}'
            """
        )
        return cursor_.fetchone()


def check_if_item_id_in_table(items_ids):
    sql_or_string = ' OR '.join([f"id='{x}'" for x in items_ids])
    with DatabaseManager() as cursor_:
        cursor_.execute(
            f"""
            SELECT id from {Constants.menu_database_name.value}
            where {''.join(sql_or_string)}
            """
        )
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


def insert_replace_address(data_dict):
    with DatabaseManager() as cursor_:
        cursor_.execute(
            f"""
            INSERT INTO {Constants.address_database_name.value} 
            (address, address_line_2, city, postal_code, phone_number, username, first_name, surname)
            VALUES ('{data_dict['address']}', '{data_dict['address_line_2']}', '{data_dict['city']}',
                    '{data_dict['postal_code']}', '{data_dict['phone_number']}', '{data_dict['username']}',
                    '{data_dict['first_name']}', '{data_dict['surname']}') 
            
            ON CONFLICT (username)
            DO
            UPDATE
            SET address='{data_dict['address']}', address_line_2='{data_dict['address_line_2']}', 
                city='{data_dict['city']}', postal_code='{data_dict['postal_code']}',
                 phone_number='{data_dict['phone_number']}', username='{data_dict['username']}',
                 first_name='{data_dict['first_name']}', surname='{data_dict['surname']}'
            """
        )


def inset_into_order_table(data_dict):
    with DatabaseManager() as cursor_:
        cursor_.execute(
            f"""
            INSERT INTO {Constants.order_database_name.value}
            VALUES ('{data_dict['status']}', '{data_dict['username']}', 
                     ARRAY {data_dict['items']}, '{data_dict['order_id']}')
            """,
        )


if __name__ == '__main__':
    with DatabaseManager() as cursor:
        create_user_table(cursor)
        create_address_table(cursor)
        create_menu_table(cursor)
        create_order_table(cursor)
