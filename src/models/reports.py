from dataclasses import dataclass

@dataclass
class Report:
    id:str
    category:str
    description:str
    date:str
    user_id:str
    comment_id:str
    thread_id:str