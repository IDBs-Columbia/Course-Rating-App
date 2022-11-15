from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
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
    has_rated = course_repository.check_user_rate_course(session['user']['id'], call_number)
    print(has_rated)
    if has_rated.get('has_rated'):
        return "You have already rated this course."

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

    return render_template("review.html", course=course, threads=threads,user=session.get('user', None))

@bp.route("/<string:call_number>", methods=["POST"])
def add_thread(call_number):
    title = request.form.get("title")
    description = request.form.get("description")
    user_id = session.get("user").get("id")

    print(title, description, user_id, call_number)
    thread_repository.add_thread(title, description, user_id, call_number)

    return redirect(url_for("course.get_course_detail", call_number=call_number,user=session.get('user', None)))
