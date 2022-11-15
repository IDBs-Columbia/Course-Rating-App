from flask import Blueprint, render_template, jsonify, session, redirect, url_for, request
from dbservice import thread_repository, comment_repository, report_repository
from models.thread import Thread
from models.comment import Comment
from datetime import date


import os


bp = Blueprint(
    "thread",
    __name__,
    url_prefix="/thread"
)


@bp.route("/<int:id>")
def get_thread_detail(id):
    thread = thread_repository.get_thread_by_id(id)
    if 'user' in session:
        rated, liked = thread_repository.check_user_like_thread(session['user']['id'], id)
    else:
        rated, liked = False, False
    comments = comment_repository.find_main_comment_by_thread(id)

    # comments = Comment.comment_list(comments)
    # comments = Comment.get_comment_by_thread_id(id)
    # todo: Comment actually has a recursive structure (comment - subcomment - subsub comment...)
    # todo: How to recursively rendering sub comments with Jinja?
    return render_template("thread.html", thread=thread, comments=comments, user=session.get('user', None),
                           rated=rated, liked=liked)

@bp.route("/<int:id>", methods=['POST'])
def add_comment(id):
    thread_id = id
    comment = request.form.get('comment')
    reply_id = request.form.get('reply_id', "null")
    user_id = session.get('user').get("id")

    comment_repository.add_comment(comment, user_id, thread_id, reply_id)
    return redirect(url_for('thread.get_thread_detail', id=id))


@bp.route("/new/<string:call_number>", methods=["POST"])
def add_new_thread(call_number):
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    uid = session['user']['id']

    if session['user']['status'] != "unrestricted":
        return "Your user group cannot add thread."

    title, desc = request.form['thread_title'], request.form['thread_description']
    if len(title.strip()) == 0 or len(desc.strip()) == 0:
        return "Please enter title and your content"
    thread_repository.add_new_thread(title, desc, date.today(), uid, call_number)
    return "Your thread has successfully published!"



@bp.route("/like/<int:tid>", methods=["POST"])
def like_thread(tid):
    if request.method == "POST":
        if 'user' not in session:
            return render_template("login.html", error="You have to login to like a course")
        uid = session['user']['id']

        if session['user']['status'] != "unrestricted":
            return "Your user group cannot like thread."

        thread_repository.user_rate_thread(uid, tid, True)
        return redirect(url_for("thread.get_thread_detail", id=tid))


@bp.route("/dislike/<int:tid>", methods=["POST"])
def dislike_thread(tid):
    print("disliked")
    if request.method == "POST":
        if 'user' not in session:
            return redirect(url_for("auth.login"))
        uid = session['user']['id']

        if session['user']['status'] != "unrestricted":
            return "Your user group cannot dislike thread."

        thread_repository.user_rate_thread(uid, tid, False)
        return redirect(url_for("thread.get_thread_detail", id=tid))


@bp.route("/report/<int:tid>", methods=["POST"])
def report_thread(tid):
    if 'user' not in session:
        return render_template("login.html", error="You are not logged in.")
    uid = session['user']['id']

    if report_repository.user_has_reported_thread(uid, tid):
        return "You have already reported this thread!"

    cates = {"0": "untruthful comment", "1": "hate speech", "2": "academic misconduct"}
    cate = cates[request.form['report_category']]
    desc = request.form['report_description']
    report_repository.user_report_thread(uid, tid, cate, desc, date.today())
    return "report success!"
