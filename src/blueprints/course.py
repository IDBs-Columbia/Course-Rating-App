from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from dbservice import course_repository, thread_repository
from models.course import Course
import os

relative_static_folder = os.environ.get("STATIC_FOLDER")
static_folder = os.path.abspath('../frontend/assets')

bp = Blueprint(
    "course",
    __name__,
    static_folder=static_folder,
    url_prefix="/course")


@bp.route("/list")
def list_all_courses():
    res = course_repository.get_all_courses()
    return render_template("courses.html")


@bp.route("/liststat")
def list_all_courses_with_stat():
    courses = course_repository.get_all_courses_with_stat()
    return render_template("courses.html", courses=courses)


@bp.route("/<string:call_number>", methods=["GET"])
def get_course_detail(call_number):
    course = course_repository.get_course_with_stat(call_number)
    threads = thread_repository.find_all_thread_by_course(call_number)
    course = Course(course)

    return render_template("review.html", course=course, threads=threads)

@bp.route("/<string:call_number>", methods=["POST"])
def add_thread(call_number):
    title = request.form.get("title")
    description = request.form.get("description")
    user_id = session.get("user").get("id")

    print(title, description, user_id, call_number)
    thread_repository.add_thread(title, description, user_id, call_number)

    return redirect(url_for("course.get_course_detail", call_number=call_number))
