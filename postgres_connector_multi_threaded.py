from psycopg2.extras import RealDictCursor           # api to connect to postgres database
from psycopg2.pool import ThreadedConnectionPool     # importing api for Multithreading
import logging      
import json                                # api for logs

logger = logging.getLogger()


class ConnectionType(object):
    RESEARCHER = 'postgres'


class PostgresConnector(object):            # class that connects to database
    _instance_dict = {}

    MIN_CONN, MAX_CONN = 1, 8               # max and min thread counts

    def __new__(cls, connection_type):     #creating a self instance
#creating a insgance that connects with database if its not present 
#else returning the instance wich is already present
        if cls._instance_dict.get(connection_type) is None:
            cls._instance_dict[connection_type] = object.__new__(cls)
            cls._instance_dict[connection_type].__pool = None
            db_config = {
                'dbname': "downloads",
                'host': "127.0.0.1",
                'password': 'amn',
                'port': '5432',
                'user': 'postgres',
                'cursor_factory': RealDictCursor,
                'sslmode': 'disable'
            }
            PostgresConnector._instance_dict[connection_type].__pool = ThreadedConnectionPool(
                minconn=PostgresConnector.MIN_CONN, maxconn=PostgresConnector.MAX_CONN, **db_config)
        return cls._instance_dict[connection_type]

    def __init__(self, connection_type=ConnectionType.RESEARCHER):   # initializing
        self.__pool = self._instance_dict[connection_type].__pool

    def _get_connection(self):
        return self.__pool.getconn()

    def _put_connection(self, connection):
        self.__pool.putconn(connection)
        
        # following are the functions for different types of queries
    def get(self, query, args=None):   # for query which returns single row
        conn = self._get_connection()
        curr = conn.cursor()
        curr.execute(query, vars=(args or ()))
        result = curr.fetchone()
        self._put_connection(conn)
        
        return result

    def execute(self, query, args=None):   # for query whose return value is not required
        conn = self._get_connection()
        curr = conn.cursor()
        curr.execute(query, vars=(args or ()))
        print("hi",query)
        conn.commit()
        self._put_connection(conn)

    def get_all(self, query, args=None):   # for query which returns multiple rows
        conn = self._get_connection()
        curr = conn.cursor()
        curr.execute(query, vars=(args or ()))
        result = curr.fetchall()
        self._put_connection(conn)
        return result

    def __del__(self):          # to close all the threads
        if self.__pool is not None:
            self.__pool.closeall()


res_con=PostgresConnector(ConnectionType.RESEARCHER)
query='''update  download_datas set value=%s where uid=%s'''
value = {"finished": 1, "remaining":2}
value=json.dumps(value)
print(value)
res_con.execute(query,(value,1))

