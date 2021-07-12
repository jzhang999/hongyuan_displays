import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory, json)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('products', __name__)


@bp.route('/products')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, product_name, description, created, author_id, username, pic_name'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('products/index.html', posts=posts)


@bp.route('/product_search', methods=('GET', 'POST'))
def product_search():
    if request.method == 'POST':
        search_key = json.loads(request.values.get("search_key"))
        key = search_key["input"]

    posts = get_post(key)
    dicts = []
    for result in posts:
        dicts.append(dict(result))

    return json.dumps(dicts)


@bp.route('/product_search_id', methods=('GET', 'POST'))
def product_search_id():
    if request.method == 'POST':
        search_id = json.loads(request.values.get("product_id"))

    posts = get_post_id(search_id)
    dicts = []
    for result in posts:
        dicts.append(dict(result))

    return json.dumps(dicts)


@bp.route('/recommendation', methods=('GET', 'POST'))
def recommendation():
    posts = get_post_rec()
    dicts = []
    for result in posts:
        dicts.append(dict(result))

    return json.dumps(dicts)


def get_post(key):
    posts = get_db().execute(
        ' SELECT p.id, product_name, description, created, pic_name, category'
        ' FROM product p'
        ' WHERE product_name LIKE ?',
        ('%'+key+'%',)
    ).fetchall()

    if posts is None:
        abort(404, f"Post id {id} doesn't exist.")

    return posts


def get_post_id(id):
    posts = get_db().execute(
        ' SELECT p.id, product_name, description, created, pic_name, category'
        ' FROM product p'
        ' WHERE id == ?',
        (id,)
    ).fetchall()

    if posts is None:
        abort(404, f"Post id {id} doesn't exist.")

    return posts


def get_post_rec():
    posts = get_db().execute(
        ' SELECT p.id, product_name, description, created, pic_name, category'
        ' FROM product p'
        ' WHERE recommend == "是"'
    ).fetchall()

    if posts is None:
        abort(404, f"Post id {id} doesn't exist.")

    return posts