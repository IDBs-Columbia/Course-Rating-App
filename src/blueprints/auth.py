from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from dbservice import user_repository

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if 'user' not in session:
            return render_template("login.html")
        else:
            return redirect(url_for("course.list_all_courses_with_stat"))
    if request.method == "POST":
        email, pw = request.form["email"], request.form["password"]
        res = user_repository.validate_login(email, pw)

        if res:
            email, status, name = user_repository.get_user_info_by_email(email)
            if status == "banned":
                return render_template("login.html", error="You account has been suspended")
            session['user'] = [email, status, name, id]
            return redirect(url_for("course.list_all_courses_with_stat"))
        else:
            return render_template("login.html", error="Invalid email/password.")


@bp.route("/logout", methods=["GET"])
def logout():
    if 'user' not in session:
        return render_template("login.html", error="You are not logged in.")

    session.pop('user')
    return render_template("login.html", error="You have successfully logged out.")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if 'user' in session:
            return redirect(url_for("course.list_all_courses_with_stat"))
        else:
            return render_template("register.html")
    if request.method == "POST":
        email, pw, pwr = request.form["email"], request.form["password"], request.form["password_repeat"]
        if pw != pwr:
            return render_template("register.html", error="Please make sure you entered the same password.")
        if user_repository.check_email_duplicate(email):
            return render_template("register.html", error="This email has already been registered.")
        res = user_repository.create_new_user(email, pw)
        if res:
            return render_template("login.html", error="Register Success! Now you can log in.")
        else:
            return render_template("register.html", error="Unknown error happened, please try again.")
