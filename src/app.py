from flask import Flask, redirect, render_template, \
                 request, url_for, flash

from blueprints.index import bp as index_bp
from blueprints.course import bp as course_bp
from blueprints.thread import bp as thread_bp
from utils.json_encoder import MyJSONEncoder

import os

template_folder = os.path.abspath('../frontend')
static_folder = os.path.abspath('../frontend/assets')

app = Flask(
    __name__,
    template_folder = template_folder,
    static_folder = static_folder
)

app.json_provider_class = MyJSONEncoder
app.register_blueprint(index_bp)
app.register_blueprint(course_bp)
app.register_blueprint(thread_bp)
app.secret_key = 'any random string'

@app.route('/review', methods = ['GET'])
def get_class(classname:str):
    return render_template('review.html', classname=classname)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = "Invalid email or password. Please try again!"

        # TODO: check if user exists in database
        # TODO: check if password is correct
        # TODO: if both are correct, redirect to home page

        return redirect(url_for('index'))
    else:
        flash('You were successfully logged in')
        return render_template('login.html', error = error)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            error = "Passwords do not match. Please try again!"
            return render_template('register.html', error = error)
        else:    
            # TODO: check if user exists in database  
            flash('You were successfully registered')
            return redirect(url_for('index'))
    else:
        return render_template('register.html', error = error)

# @app.route('/<usr>')
# def user(usr):
#     return f'<h1>Hello {usr}</h1>'

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8111,
        debug=True
    )
