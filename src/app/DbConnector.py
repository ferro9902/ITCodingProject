import psycopg2
import ConfigLoaders.DbConfigLoader


class DbConnector:
    def __init__(self):
        cl = ConfigLoaders.DbConfigLoader.DbConfigLoader()

        self.ip = cl.get_param("ip")
        self.port = cl.get_param("port")
        self.db = cl.get_param("db")
        self.user = cl.get_param("user")
        self.psw = cl.get_param("psw")
        self.conn = None

        # connection initialization
        try:
            self.conn = psycopg2.connect(
                host=self.ip,
                port=self.port,
                database=self.db,
                user=self.user,
                password=self.psw
            )
            print("DB connection successful")
        except (Exception, psycopg2.Error) as error:
            print("DB connection threw the following error:", error)

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Disconnected from DB")

    def query_db(self, query: str) -> list:
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            print(
                f"found [{len(records)}] records from query: {query}")
            return records
        except (Exception, psycopg2.Error) as error:
            print("Query Error:", error)
            return None
