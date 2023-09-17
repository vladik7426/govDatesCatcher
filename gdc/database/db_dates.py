from dataclasses import dataclass

from datetime import datetime

from gdc.database.__executor import execute_query


@dataclass
class DataDate:
    bdid: int
    datetime: datetime
    client_id: int


def write_date(data: DataDate) -> bool:
    return execute_query("INSERT INTO `dates` (`datetime`, `client_id`) VALUES (%s, %s);",
                         (data.datetime,
                          data.client_id))
