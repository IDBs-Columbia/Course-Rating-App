from flask import Blueprint, render_template, request
import os


bp = Blueprint(
    "index",
    __name__,
    url_prefix="/"
)

@bp.route('/', methods = ['GET'])
def index():

    template_vars = {
        'account_id': request.cookies.get('account_id'),
        'account_url': request.cookies.get('account_url')
    }

    return render_template('index.html', **template_vars)
