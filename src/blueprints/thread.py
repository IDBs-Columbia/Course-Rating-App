from flask import Blueprint, render_template, jsonify
from dbservice import thread_repository, comment_repository
from models.thread import Thread

bp = Blueprint("thread", __name__, url_prefix="/thread")


@bp.route("/<int:id>")
def get_thread_detail(id):
    thread = thread_repository.get_thread_by_id(id)
    comments = comment_repository.find_main_comment_by_thread(id)
    
    thread = Thread(thread)

    # todo: Comment actually has a recursive structure (comment - subcomment - subsub comment...)
    # todo: How to recursively rendering sub comments with Jinja?
    return render_template("thread.html", thread=thread, comments=comments)
