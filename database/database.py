import sqlite3
from .queries import Queries


class Database:
    def __init__(self, path):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(Queries.CREATE_SURVEY_TABLE)
            conn.commit()

    def execute(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.path) as conn:
            conn.execute(query, params)
            conn.commit()

    def fetchall(self, query: str, params: tuple = (), fetchall: bool = True):
        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row
            data = conn.execute(query, params)

            if fetchall:
                result = data.fetchall()
                if not result:
                    return None
                return [dict(row) for row in result]
            else:
                result = data.fetchone()
                if not result:
                    return None
                return dict(result)