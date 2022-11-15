from datetime import date

from flask import Blueprint, session, render_template, request, redirect, url_for

from dbservice import report_repository, comment_repository

bp = Blueprint("comment", __name__, url_prefix="/comment")


@bp.route("/report/<int:cid>", methods=["POST"])
def report_comment(cid):
    if 'user' not in session:
        return render_template("login.html", error="You are not logged in.")
    uid = session['user']['id']
    if report_repository.user_has_reported_comment(uid, cid):
        return "You have already reported this comment!"

    cates = {"0": "untruthful comment", "1": "hate speech", "2": "academic misconduct"}
    cate = cates[request.form['report_category']]
    desc = request.form['report_description']
    report_repository.user_report_comment(uid, cid, cate, desc, date.today())
    return "report success!"


@bp.route("/new/<string:tid>", methods=["POST"])
def add_new_comment(tid):
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    uid = session['user']['id']

    if session['user']['status'] != "unrestricted":
        return "Your user group cannot add comment."

    content = request.form['comment_content']
    if len(content.strip()) == 0:
        return "Please enter your content"

    comment_repository.add_new_comment(content, date.today(), uid, tid)

    return "Your comment has successfully published!"
