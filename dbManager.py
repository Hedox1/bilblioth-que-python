import psycopg2
from config import getDBConfig


class DbManager:

    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            params = getDBConfig()

            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def execute_query(self, query, data=None):
        """ Execute a query and return the result """
        result = None
        try:
            # create a cursor
            cur = self.conn.cursor()

            # execute the query with optional data
            if data:
                cur.execute(query, data)
            else:
                cur.execute(query)

            # commit the transaction
            self.conn.commit()

            # fetch the result if applicable
            if cur.description is not None:
                result = cur.fetchall()

            # close the cursor
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return result

    def get_data(self, table_name: str, fields=["*"], where: str = None, join: list[str] = None):
        request = f'Select {",".join(fields)} from {table_name} '
        if where:
            request += f'where {where} '
        if join:
            request += f'join {" join ".join(join)} '

        print(request)
        return self.execute_query(request)

    def insert_data(self, table_name: str, values: dict[str, str]):
        request = f'insert into {table_name} ({",".join(list(values.keys()))}) values ({",".join(list(values.values()))})'
        print(request)
        return self.execute_query(request)

    def update_data(self, table_name: str, values: dict[str, str], where: str = None):
        request = f'update {table_name} set {", ".join(f"{key} = {value}" for key, value in values.items())} '
        request += f'where {where} '
        print(request)
        return self.execute_query(request)

    def delete_data(self, table_name: str, where: str):
        request = f'delete from {table_name} where {where}'
        print(request)
        return self.execute_query(request)
