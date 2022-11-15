from dbservice import institution_repository
from dataclasses import dataclass

@dataclass
class Institution:
    id:str
    name:str

    def __init__(self, query_result):
        for key, value in query_result.items():
            self.__set_value(key, value)

    def __set_value(self, key, value):
        if key == 'id':
            self.id = value
        elif key == 'institution_name':
            self.name = value

    @staticmethod
    def get_institution_list(results):
        institution_list = []
        for result in results:
            institution_list.append(Institution(result))
        return institution_list

    @staticmethod
    def get_institutions():
        results = institution_repository.get_institutions()
        return Institution.get_institution_list(results)