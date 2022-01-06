import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory, json)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('categories', __name__)


@bp.route('/categories')
def index():
    db = get_db()
    posts = db.execute(
        ' SELECT cat_name, cat_icon_name'
        ' FROM category'
        ' ORDER BY cat_name DESC'
    ).fetchall()
    return render_template('categories/index.html', posts=posts)


@bp.route('/cat_search', methods=('GET', 'POST'))
def cat_search():
    if request.method == 'POST':
        search_key = json.loads(request.values.get("search_key"))

    posts = get_post(search_key)
    dicts = []
    for result in posts:
        dicts.append(dict(result))

    return json.dumps(dicts)


@bp.route('/get_all_cat_names', methods=('GET', 'POST'))
def get_all_cat_names():
    db = get_db()
    cats = db.execute(
        ' SELECT cat_name'
        ' FROM category'
    ).fetchall()

    dicts = []
    for result in cats:
        dicts.append(result)

    results = []
    for dict in dicts:
        results.append(dict["cat_name"])

    return json.dumps(results)

@bp.route('/get_all_cat_objs', methods=('GET', 'POST'))
def get_all_cat_objs():
    db = get_db()
    cats = db.execute(
        ' SELECT *'
        ' FROM category'
    ).fetchall()

    dicts = []
    for result in cats:
        dicts.append(dict(result))

    # results = []
    # for dict in dicts:
    #     results.append(dict["cat_name"])

    return json.dumps(dicts)


def get_post(key):
    posts = get_db().execute(
        ' SELECT p.id, product_name, description, created, pic_name0, category'
        ' FROM product p JOIN category c ON p.category = c.cat_name'
        ' WHERE cat_name == ?'
        ' ORDER BY created DESC',
        (key,)
    ).fetchall()

    if posts is None:
        abort(404, f"Post id {id} doesn't exist.")

    return posts
