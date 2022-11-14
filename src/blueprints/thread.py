from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from dbservice import thread_repository, comment_repository

bp = Blueprint("thread", __name__, url_prefix="/thread")


@bp.route("/<int:id>")
def get_thread_detail(id):
    thread = thread_repository.get_thread_by_id(id)
    comments = comment_repository.find_main_comment_by_thread(id)

    # todo: Comment actually has a recursive structure (comment - subcomment - subsub comment...)
    # todo: How to recursively rendering sub comments with Jinja?
    return render_template("thread.html", thread=thread, comments=comments)

@bp.route("/new/<string:call_number>", methods=["POST"])
def add_new_thread(call_number):
    pass

@bp.route("/like/<int:thread_id>")
def like_thread(thread_id):
    if 'user' not in session:
        return render_template("login.html", error="You have to login to like a course")
    email, status, name, uid = session['user']
    if thread_repository.check_user_rated_email(uid, thread_id):
        return redirect(url_for("get_thread_detail", thread_id))
