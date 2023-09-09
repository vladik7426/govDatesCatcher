from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from pymysql.cursors import Cursor


@dataclass
class DataBaseData(ABC):
    """
    Just an abstract class.
    """
    @staticmethod
    @abstractmethod
    def fetchone(cursor: Cursor):
        """
        Fetches cursors one data row and formats to self type.
        :param cursor: that already select data
        :return: self type
        """
        pass

    @staticmethod
    @abstractmethod
    def fetchall(cursor: Cursor):
        """
        Fetches cursors all data rows and formats to self type.
        :param cursor: that already select data
        :return: list with self types
        """
        pass


@dataclass
class DataClient(DataBaseData):
    bdid: int
    name: str
    surname: str
    thirdname: str
    phone: str
    email: str
    registered: bool

    @staticmethod
    def fetchone(cursor: Cursor):
        return DataClient(*cursor.fetchone())

    @staticmethod
    def fetchall(cursor: Cursor):
        return [DataClient(*row) for row in cursor.fetchall()]


@dataclass
class DataDate(DataBaseData):
    bdid: int
    datetime: datetime
    client_id: int

    @staticmethod
    def fetchone(cursor: Cursor):
        return DataDate(*cursor.fetchone())

    @staticmethod
    def fetchall(cursor: Cursor):
        return [DataDate(*row) for row in cursor.fetchall()]
