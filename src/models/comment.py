from dataclasses import dataclass
from dbservice import comment_repository
from dbservice import user_repository

@dataclass
class Comment():
    comment_id: str
    content: str
    date: str
    reply_id: str
    user_id: str
    thread_id: str
    likes: int = 0
    dislikes: int = 0
    author: str = None
    reply_author: str = None

    def __init__(self, query_result:dict):

        for key, value in query_result.items():
            self.__set_values(key, value)

    def __set_values(self, key, value):
        if key == "id":
            self.comment_id = value
        elif key == "content":
            self.content = value
        elif key == "likes":
            self.likes = value
        elif key == "dislikes":
            self.dislikes = value
        elif key == "date":
            self.date = value
        elif key == "reply_id":
            self.reply_id = value
        elif key == "user_id":
            self.user_id = value
        elif key == "thread_id":
            self.thread_id = value

    def to_dict(self):
        return {
            "id": self.comment_id,
            "content": self.content,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "date": self.date,
            "reply_id": self.reply_id,
            "user_id": self.user_id,
            "thread_id": self.thread_id
        }

    @staticmethod
    def comment_list(query_result):
        if query_result is None:
            return None

        comment_list = []
        for result in query_result:
            comment_list.append(Comment(result))
            sub = result.get("sub")
            if sub:
                subs = Comment.comment_list(sub)
                comment_list.extend(subs)

        return comment_list

    @staticmethod
    def get_comment_by_thread_id(id):
        results = comment_repository.find_main_comment_by_thread(id)
        comments = Comment.comment_list(results)
        
        authors = {}
        for comment in comments:
            # Add comment author names
            author = user_repository.get_user_name_by_id(comment.user_id)
            if author:
                authors[comment.comment_id] = comment.user_id
                comment.author = author.get("name")

            # Add reply author names
            if comment.reply_id:
                reply_author_id = authors.get(comment.reply_id)
                reply_author = user_repository.get_user_name_by_id(reply_author_id)
                if reply_author:
                    comment.reply_author = reply_author.get("name")
                
        return comments

    