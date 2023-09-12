from dataclasses import dataclass

from gdc_database.__executor import execute_query_all, execute_query


@dataclass
class DataClient:
    bdid: int
    name: str
    surname: str
    thirdname: str
    phone: str
    email: str
    consulate: str
    category: str
    registered: bool


def get_unreg_clients() -> list[DataClient]:
    return execute_query_all("SELECT * FROM `clients` WHERE `registered`=0", fetching_class=DataClient)


def update_client(data: DataClient) -> bool:
    return execute_query("UPDATE clients "
                         f"SET name=%s, surname=%s, thirdname=%s, phone=%s, email=%s, consulate=%s, category=%s, "
                         f"registered=%s WHERE id={data.bdid};", (data.name,
                                                                  data.surname,
                                                                  data.thirdname,
                                                                  data.phone,
                                                                  data.email,
                                                                  data.consulate,
                                                                  data.category,
                                                                  data.registered))
