from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for
from dbservice import course_repository, thread_repository
from models.course import Course
import os

bp = Blueprint(
    "course",
    __name__,
    url_prefix="/course")


@bp.route("/list")
def list_all_courses():
    res = course_repository.get_all_courses()
    return render_template("courses.html")


@bp.route("/liststat")
def list_all_courses_with_stat():
    courses = course_repository.get_all_courses_with_stat()
    return render_template("courses.html", courses=courses, user=session.get('user', None))

@bp.route("/rate/<string:call_number>", methods=["POST"])
def user_rate_course(call_number):
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    f = request.form
    rating, workload, difficulty = f['rating'], f['workload'], f['difficulty']
    uid = session['user']['id']
    if session['user']['status'] != "unrestricted":
        return "Your user group cannot rate course."

    course_repository.add_user_rating(call_number, rating, workload, difficulty, uid)

    return "rating successfully submitted!"

@bp.route("/<string:call_number>", methods=["GET"])
def get_course_detail(call_number):
    course = course_repository.get_course_with_stat(call_number)
    threads = thread_repository.find_all_thread_by_course(call_number)

    return render_template("review.html", course=course, threads=threads)



