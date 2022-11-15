from dataclasses import dataclass
from dbservice import reports_repository

@dataclass
class Report:
    id:str
    category:str
    description:str
    date:str
    user_id:str
    comment_id:str
    thread_id:str

    def __init__(self, query_result):
        for key, value in query_result.items():
            self.__set_value(key, value)

    def __set_value(self, key, value):
        if key == 'id':
            self.id = value
        elif key == 'category':
            self.category = value
        elif key == 'description':
            self.description = value
        elif key == 'date':
            self.date = value
        elif key == 'user_id':
            self.user_id = value
        elif key == 'comment_id':
            self.comment_id = value
        elif key == 'thread_id':
            self.thread_id = value

    @staticmethod
    def get_report_list(results):
        report_list = []
        for result in results:
            report_list.append(Report(result))
        return report_list

    @staticmethod
    def get_reports():
        results = reports_repository.get_reports()
        return Report.get_report_list(results)
