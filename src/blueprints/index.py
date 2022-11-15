from flask import Blueprint, render_template, request, redirect, url_for
import os


bp = Blueprint(
    "index",
    __name__,
    url_prefix="/"
)

@bp.route('/', methods = ['GET'])
def index():
    return redirect(url_for("course.list_all_courses_with_stat"))