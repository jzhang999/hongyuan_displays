import os
import datetime

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

@bp.route('/cat_create', methods=('GET', 'POST'))
@login_required
def cat_create():
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        error = None

        pic0 = request.files['file0']
        pic_name0 = str(datetime.datetime.now()) + '@' + pic0.filename
        pic0.save(
            os.path.join("/var/www/hongyuan_displays/flaskr/static/uploaded_files", pic_name0))

        if not cat_name:
            error = 'Category name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO category (cat_name, cat_icon_name)'
                ' VALUES (?, ?)',
                (cat_name, pic_name0)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('categories/cat_create.html')

@bp.route('/<string:cat_name>/cat_update', methods=('GET', 'POST'))
@login_required
def cat_update(cat_name):
    post = get_db().execute(
        ' SELECT cat_name, cat_icon_name'
        ' FROM category'
        ' WHERE cat_name = ?',
        (cat_name,)
    ).fetchone()

    icon_name = post['cat_icon_name']

    if request.method == 'POST':
        new_cat_name = request.form['cat_name']
        pic0 = request.files['file0']
        error = None

        # see if the pic is changed
        if pic0.filename != "":
            os.remove(os.path.join("/var/www/hongyuan_displays/flaskr/static/uploaded_files",
                                   post['cat_icon_name']))
            icon_name = str(datetime.datetime.now()) + '@' + pic0.filename
            pic0.save(os.path.join("/var/www/hongyuan_displays/flaskr/static/uploaded_files",
                                   icon_name))
        if not cat_name:
            error = 'Category name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                ' UPDATE category SET cat_name = ?, cat_icon_name = ? '
                ' WHERE cat_name = ?',
                (new_cat_name, icon_name, cat_name,)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('categories/cat_update.html', post=post)


@bp.route('/<string:cat_name>/cat_delete', methods=('POST',))
@login_required
def cat_delete(cat_name):
    db = get_db()

    post = db.execute(
        ' SELECT cat_name, cat_icon_name'
        ' FROM category'
        ' WHERE cat_name = ?',
        (cat_name,)
    ).fetchone()

    os.remove(os.path.join("/var/www/hongyuan_displays/flaskr/static/uploaded_files",
                           post['cat_icon_name']))

    db.execute('DELETE FROM category WHERE cat_name = ?', (cat_name,))
    db.commit()
    return redirect(url_for('log.index'))

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
