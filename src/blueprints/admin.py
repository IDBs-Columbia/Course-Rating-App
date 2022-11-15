from flask import Blueprint, render_template, jsonify
from dbservice import thread_repository
from dbservice import comment_repository
from dbservice import user_repository
from dbservice import reports_repository

from models.thread import Thread
from models.comment import Comment
from models.user import User

import os

relative_static_folder = os.environ.get("STATIC_FOLDER")
static_folder = os.path.abspath('../frontend/assets')

bp = Blueprint(
    "admin",
    __name__,
    static_folder=static_folder,
    url_prefix="/admin"
)

@bp.route("/")
def get_admin_dashboard():
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
    reports = reports_repository.get_reports()
    return render_template("admin/report-dashboard.html", reports = reports)