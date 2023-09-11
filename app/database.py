from pymysql import connect

from app.database_dataclasses import DataBaseData, DataClient, DataDate

database_connection_info = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '13245',
    'database': 'govdatescatcher',
    'autocommit': True,
}


def get_unreg_clients() -> list[DataClient]:
    return _execute_query_all("SELECT * FROM `clients` WHERE `registered`=0", fetch_as=DataClient)


def update_client(data: DataClient):
    _execute_query("UPDATE clients "
                   f"SET name=%s, surname=%s, thirdname=%s, phone=%s, email=%s, registered=%s "
                   f"WHERE id={data.bdid};", (data.name,
                                              data.surname,
                                              data.thirdname,
                                              data.phone,
                                              data.email,
                                              data.registered))


def write_date(data: DataDate):
    _execute_query("INSERT INTO `dates` (`datetime`, `client_id`) VALUES (%s, %s);",
                   (data.datetime,
                    data.client_id))


def _execute_query(query, args: tuple) -> bool:
    try:
        connect(**database_connection_info).cursor().execute(query, args)
        return True
    except Exception as e:
        return False


def _execute_query_one(query, fetch_as: DataBaseData, args: tuple = ()) -> DataBaseData:
    cursor = connect(**database_connection_info).cursor()

    cursor.execute(query, args)

    return fetch_as.fetchone(cursor)


def _execute_query_all(query, fetch_as: DataBaseData, args: tuple = ()) -> list[DataBaseData]:
    cursor = connect(**database_connection_info).cursor()

    cursor.execute(query, args)

    return fetch_as.fetchall(cursor)
