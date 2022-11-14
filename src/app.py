from flask import Flask, redirect, render_template, \
                 request, url_for, flash

from blueprints.course import bp as course_bp
from blueprints.thread import bp as thread_bp
from blueprints.auth import bp as auth_bp


app = Flask(
    __name__
)

app.register_blueprint(course_bp)
app.register_blueprint(thread_bp)
app.register_blueprint(auth_bp)
app.secret_key = 'any random string'



if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8111,
        debug=True
    )
