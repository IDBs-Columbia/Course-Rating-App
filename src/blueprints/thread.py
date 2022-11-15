from flask import Blueprint, render_template, jsonify, session, redirect, url_for, request
from dbservice import thread_repository, comment_repository
from models.thread import Thread

bp = Blueprint("thread", __name__, url_prefix="/thread")


@bp.route("/<int:id>")
def get_thread_detail(id):
    thread = thread_repository.get_thread_by_id(id)
    comments = comment_repository.find_main_comment_by_thread(id)
    if 'user' in session:
        rated, liked = thread_repository.check_user_like_thread(session['user']['id'], id)
    else:
        rated, liked = False, False

    # todo: Comment actually has a recursive structure (comment - subcomment - subsub comment...)
    # todo: How to recursively rendering sub comments with Jinja?
    return render_template("thread.html", thread=thread, comments=comments, rated=rated, liked=liked)

@bp.route("/new/<string:call_number>", methods=["POST"])
def add_new_thread(call_number):
    pass

@bp.route("/like/<int:tid>", methods=["POST"])
def like_thread(tid):
    if request.method == "POST":
        if 'user' not in session:
            return render_template("login.html", error="You have to login to like a course")
        uid = session['user']['id']
        thread_repository.user_rate_thread(uid, tid, True)
        return redirect(url_for("thread.get_thread_detail", id=tid))

@bp.route("/dislike/<int:tid>", methods=["POST"])
def dislike_thread(tid):
    print("disliked")
    if request.method == "POST":
        if 'user' not in session:
            return redirect(url_for("auth.login"))
        uid = session['user']['id']
        thread_repository.user_rate_thread(uid, tid, False)
        return redirect(url_for("thread.get_thread_detail", id=tid))