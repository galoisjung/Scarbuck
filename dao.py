from sqlalchemy import create_engine


class Dao():
    def __init__(self, sql_url):
        self.sql_url = sql_url
        self.engine = create_engine(sql_url)
        