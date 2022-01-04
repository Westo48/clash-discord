import pymysql
import data.RazBotDB_Connection_Data as RazBotDB_Connection_Data


def fetch_single_query(query):

    connection_data = RazBotDB_Connection_Data.RazBotDB_Connection_Data()

    connection = pymysql.connect(
        host=connection_data.hostname,
        user=connection_data.username,
        password=connection_data.password,
        db=connection_data.db_name,
        port=connection_data.port
    )

    cur = connection.cursor()

    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    connection.close()
    return result


def fetch_all_query(query):

    connection_data = RazBotDB_Connection_Data.RazBotDB_Connection_Data()

    connection = pymysql.connect(
        host=connection_data.hostname,
        user=connection_data.username,
        password=connection_data.password,
        db=connection_data.db_name,
        port=connection_data.port
    )

    cur = connection.cursor()

    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    connection.close()
    return result


def execute_query(query):

    connection_data = RazBotDB_Connection_Data.RazBotDB_Connection_Data()

    connection = pymysql.connect(
        host=connection_data.hostname,
        user=connection_data.username,
        password=connection_data.password,
        db=connection_data.db_name,
        port=connection_data.port
    )

    cur = connection.cursor()

    cur.execute(query)
    connection.commit()
    cur.close()
    connection.close()
