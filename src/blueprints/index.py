from flask import Blueprint, render_template, request, redirect, url_for, session
import os

relative_static_folder = os.environ.get("STATIC_FOLDER")
static_folder = os.path.abspath(relative_static_folder)

bp = Blueprint(
    "index",
    __name__,
    static_folder=static_folder,
    url_prefix="/"
)

@bp.route('/', methods = ['GET'])
def index():
    return redirect(url_for("course.list_all_courses_with_stat", user=session.get('user', None)))