from dataclasses import dataclass
from dbservice import course_repository

@dataclass
class Course:
    call_number: int
    course_number: int
    name: str
    institution_id: int
    description: str = "No description for this course."
    instructor: str = "No instructor for this course."
    satisfaction: float = 1
    workload: float = 1
    difficulty: float = 1

    def __init__(self, query_result:dict):
        for key, value in query_result.items():
            self.__set_values(key, value)

    def __set_values(self, key, value):
        if key == "call_number":
            self.call_number = value
        elif key == "course_number":
            self.course_number = value
        elif key == "name":
            self.name = value
        elif key == "description":
            self.description = value
        elif key == "instructor":
            self.instructor = value
        elif key == "institution_id":
            self.institution_id = value
        elif key == "avg_satisfaction":
            self.avg_satisfaction = value
        elif key == "avg_workload":
            self.avg_workload = value
        elif key == "avg_difficulty":
            self.avg_difficulty = value

    def update_stats(self, *stats):
        self.avg_satisfaction = stats[0]
        self.avg_workload = stats[1]
        self.avg_difficulty = stats[2]

    def to_dict(self):
        return {
            "call_number": self.call_number,
            "course_number": self.course_number,
            "course_name": self.name,
            "course_description": self.description,
            "course_instructor": self.instructor,
            "institution_id": self.institution_id,
            "course_satisfaction": self.avg_satisfaction,
            "course_workload": self.avg_workload,
            "course_difficulty": self.avg_difficulty
        }

    @staticmethod
    def course_list(query_result):
        course_list = []
        for course in query_result:
            course_list.append(Course(course))
        return course_list

    @staticmethod
    def get_courses():
        result = course_repository.get_all_courses()
        return Course.course_list(result)