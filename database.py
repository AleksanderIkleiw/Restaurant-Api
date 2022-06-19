import psycopg2
from decouple import config


class EstablishConnection:
    def __init__(self):
        conn = psycopg2.connect(
            host='localhost',
            database='restaurant',
            user='admin',
            password='admin',
            port=5432
        )
        self.cursor = conn.cursor()



class CreateTables(EstablishConnection):
    pass