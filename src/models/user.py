from dataclasses import dataclass
from dbservice import user_repository

@dataclass
class User():
    id: str
    name: str
    email: str
    strikes: int = None
    status: str = None
    can_manage_report: bool = False
    can_manage_course: bool = False
    can_manage_comment: bool = False
    can_manage_user: bool = False

    def __init__(self, query_result:dict):
        for key, value in query_result.items():
            self.__set_values(key, value)

    def __set_values(self, key, value):
        if key == "id":
            self.id = value
        elif key == "name":
            self.name = value
        elif key == "email":
            self.email = value
        elif key == "strikes":
            self.strikes = value
        elif key == "status":
            self.status = value
        elif key == "can_manage_report":
            self.can_manage_report = value
        elif key == "can_manage_course":
            self.can_manage_course = value
        elif key == "can_manage_comment":
            self.can_manage_comment = value
        elif key == "can_manage_user":
            self.can_manage_user = value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "strikes": self.strikes,
            "status": self.status,
            "can_manage_report": self.can_manage_report,
            "can_manage_course": self.can_manage_course,
            "can_manage_comment": self.can_manage_comment,
            "can_manage_user": self.can_manage_user
        }

    @staticmethod
    def user_list(query_result):
        user_list = []
        for user in query_result:
            user_list.append(User(user))
        return user_list

    @staticmethod
    def get_regular_users():
        users = user_repository.get_all_regular_users()
        return User.user_list(users)
    
    @staticmethod
    def get_staff_users():
        users = user_repository.get_all_staff_users()
        return User.user_list(users)