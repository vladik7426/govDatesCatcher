from dataclasses import dataclass

from gdc_database.__executor import execute_query_all, execute_query


@dataclass
class BotChatData:
    id: int
    chat_id: int


def get_bot_chats() -> list[BotChatData]:
    return execute_query_all("SELECT * FROM `bot_chats`", BotChatData)


def write_bot_chat(data: BotChatData) -> bool:
    return execute_query("INSERT INTO `bot_chats` ("
                         "`chat_id`) VALUES (%s)", data.chat_id)
