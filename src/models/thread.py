from dataclasses import dataclass
from dbservice import thread_repository

@dataclass
class Thread():
    thread_id: str
    title: str
    description: str
    date: str
    user_id: str
    call_number: str


    def __init__(self, query_result:dict):
        for key, value in query_result.items():
            self.__set_values(key, value)

    def __set_values(self, key, value):
        if key == "id":
            self.thread_id = value
        elif key == "title":
            self.title = value
        elif key == "description":
            self.description = value
        elif key == "date":
            self.date = value
        elif key == "user_id":
            self.user_id = value
        elif key == "call_number":
            self.call_number = value

    def to_dict(self):
        return {
            "id": self.thread_id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "user_id": self.user_id,
            "call_number": self.call_number
        }

    @staticmethod
    def thread_list(query_result):
        thread_list = []
        for thread in query_result:
            thread_list.append(Thread(thread))
        return thread_list

    @staticmethod
    def get_thread_by_id(id):
        return Thread(thread_repository.get_thread_by_id(id))

    @staticmethod
    def get_threads():
        return Thread.thread_list(thread_repository.get_threads())