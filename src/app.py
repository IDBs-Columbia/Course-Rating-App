from flask import Flask
from blueprints.course import bp as course_bp
from utils.json_encoder import MyJSONEncoder

app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.register_blueprint(course_bp)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
