from flask import Blueprint, request, session, render_template, redirect, url_for

from dbservice import user_repository, report_repository

bp = Blueprint("admin1", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
def admin_index():
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    if session['user']['status'] != "admin":
        return "Regular users are not allowed to access admin board."

    permission = user_repository.get_admin_permision(session['user']['email'])

    reports = report_repository.get_all_report()

    return render_template("admin.html", permission=permission, reports=reports, user=session.get('user', None))
