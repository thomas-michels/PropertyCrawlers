from psycopg import Connection
from psycopg.rows import dict_row
from .base_connection import DBConnection
from app.core.configs import get_environment

_env = get_environment()


class PGConnection(DBConnection):

    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def execute(self, sql_statement: str, values: dict = None, all: bool = False):
        sql = sql_statement.replace("public", _env.ENVIRONMENT)

        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(sql, values)
            return cursor.fetchall() if all else cursor.fetchone()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
