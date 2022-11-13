from flask import Blueprint, jsonify
from dbservice import course_repository

bp = Blueprint("course", __name__, url_prefix="/course")

@bp.route("/list")
def list_all_courses():
    res = course_repository.get_all_courses()
    return jsonify(res)

@bp.route("/liststat")
def list_all_courses_with_stat():
    res = course_repository.get_all_courses_with_stat()
    return jsonify(res)
