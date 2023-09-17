from pymysql import connect

from gdc.database import database_connection_info


def execute_query(query, args: tuple) -> bool:
    try:
        connect(**database_connection_info).cursor().execute(query, args)
        return True
    except Exception as e:
        return False


def execute_query_one(query, fetching_class, args: tuple = ()):
    cursor = connect(**database_connection_info).cursor()

    cursor.execute(query, args)

    result = cursor.fetchone()

    return fetching_class(*result) if result is not None else None


def execute_query_all(query, fetching_class, args: tuple = ()):
    cursor = connect(**database_connection_info).cursor()

    cursor.execute(query, args)

    return [fetching_class(*row) for row in cursor.fetchall()]
