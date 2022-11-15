from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from dbservice import thread_repository, comment_repository
from models.thread import Thread
from models.comment import Comment


import os

relative_static_folder = os.environ.get("STATIC_FOLDER")
static_folder = os.path.abspath(relative_static_folder)

bp = Blueprint(
    "thread",
    __name__,
    static_folder=static_folder,
    url_prefix="/thread"
)


@bp.route("/<int:id>")
def get_thread_detail(id):
    thread = Thread.get_thread_by_id(id)
    # comments = comment_repository.find_main_comment_by_thread(id)

    # comments = Comment.comment_list(comments)
    comments = Comment.get_comment_by_thread_id(id)
    # todo: Comment actually has a recursive structure (comment - subcomment - subsub comment...)
    # todo: How to recursively rendering sub comments with Jinja?
    return render_template("thread.html", thread=thread, comments=comments)

@bp.route("/<int:id>", methods=['POST'])
def add_comment(id):
    thread_id = id
    comment = request.form.get('comment')
    reply_id = request.form.get('reply_id', "null")
    user_id = session.get('user').get("id")

    comment_repository.add_comment(comment, user_id, thread_id, reply_id)
    return redirect(url_for('thread.get_thread_detail', id=id))
