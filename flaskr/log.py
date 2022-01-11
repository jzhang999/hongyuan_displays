import os
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('log', __name__)


# / means the first page?
@bp.route('/')
def index():
    return render_template('log/index.html')


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory("/var/www/hongyuan_displays/flaskr/static/uploaded_files", filename)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, product_name, description, created, author_id, username, category, recommend, pic_name0, pic_name1, pic_name2, accessories'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

