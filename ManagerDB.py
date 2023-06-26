import psycopg2

class ManagerDB():

    _instance = None  # Singleton instance
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls) #super(ManagerDB, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.hostname = "localhost"
        self.database = "postgres"
        self.username = "postgres"
        self.pwd = "8.PosGre.8"
        self.port_id = "5432"

    def my_query(self, query, par=None):
        conn = None
        cur = None

        try:
            conn = psycopg2.connect(
                host=self.hostname,
                dbname=self.database,
                user=self.username,
                password=self.pwd,
                port=self.port_id
            )
            cur = conn.cursor()
            if par is None:
                cur.execute(query)
            else:
                cur.execute(query, par)
            conn.commit()
            return cur.fetchall()
        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

