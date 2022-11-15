from flask import Blueprint,render_template, jsonify, request, redirect, url_for, session
from dbservice import thread_repository
from dbservice import comment_repository
from dbservice import user_repository
from dbservice import reports_repository
from dbservice import institution_repository

from models.thread import Thread
from models.comment import Comment
from models.user import User
from models.reports import Report
from models.institution import Institution

import os

relative_static_folder = os.environ.get("STATIC_FOLDER")
static_folder = os.path.abspath('../frontend/assets')

bp = Blueprint(
    "admin",
    __name__,
    static_folder=static_folder,
    url_prefix="/admin"
)

def get_permissions(session):
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    if session['user']['status'] != "admin":
        return "Regular users are not allowed to access admin board."

    permission = user_repository.get_admin_permision(session['user']['email'])
    return permission

@bp.route("/")
def get_admin_dashboard():
    permission = get_permissions(session)
    return render_template("admin/dashboard.html")


@bp.route("/users/regular")
def get_regular_users():

    users = User.get_regular_users()
    return render_template("admin/user-dashboard.html", users = users)

@bp.route("/users/staff")
def get_staff_users():

    users = User.get_staff_users()
    return render_template("admin/staff-dashboard.html", users = users)

@bp.route("/reports")
def get_reports():
    reports = Report.get_reports()
    return render_template("admin/report-dashboard.html", reports = reports)

@bp.route("/institutions")
def get_institutions():
    institutions = Institution.get_institutions()
    return render_template("admin/institution-dashboard.html", institutions = institutions)

@bp.route("/institutions", methods = ['POST'])
def add_institutions():
    institution_name = request.form.get('institution_name')
    institution_repository.add_institution(institution_name)
    return redirect(url_for('admin.get_institutions'))

# from flask import Blueprint, request, session, render_template, redirect, url_for

# from dbservice import user_repository, report_repository

# bp = Blueprint("admin1", __name__, url_prefix="/admin")


# @bp.route("/", methods=["GET"])
# def admin_index():
#     if 'user' not in session:
#         return redirect(url_for("auth.login"))
#     if session['user']['status'] != "admin":
#         return "Regular users are not allowed to access admin board."

#     permission = user_repository.get_admin_permision(session['user']['email'])

#     reports = report_repository.get_all_report()

#     return render_template("admin.html", permission=permission, reports=reports, user=session.get('user', None))
