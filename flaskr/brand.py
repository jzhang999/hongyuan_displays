import os
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory, json)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('brand', __name__)


@bp.route('/brand')
def index():
    db = get_db()
    posts = db.execute(
        ' SELECT brand_name, brand_icon_name'
        ' FROM brands'
        ' ORDER BY brand_name DESC'
    ).fetchall()
    return render_template('brand/index.html', posts=posts)

@bp.route('/brand_create', methods=('GET', 'POST'))
@login_required
def brand_create():
    if request.method == 'POST':
        brand_name = request.form['brand_name']
        error = None

        pic0 = request.files['file0']
        pic_name0 = str(datetime.datetime.now()) + '@' + pic0.filename
        pic0.save(
            os.path.join("/var/www/hongyuan_displays/flaskr/static/uploaded_files", pic_name0))

        if not brand_name:
            error = 'Brand name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO brands (brand_name, brand_icon_name)'
                ' VALUES (?, ?)',
                (brand_name, pic_name0)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('brand/brand_create.html')

@bp.route('/<string:brand_name>/brand_update', methods=('GET', 'POST'))
@login_required
def brand_update(brand_name):
    post = get_db().execute(
        ' SELECT brand_name, brand_icon_name'
        ' FROM brands'
        ' WHERE brand_name = ?',
        (brand_name,)
    ).fetchone()

    icon_name = post['brand_icon_name']

    if request.method == 'POST':
        new_brand_name = request.form['brand_name']
        pic0 = request.files['file0']
        error = None

        # see if the pic is changed
        if pic0.filename != "":
            os.remove(os.path.join("/var/www/hongyuan_displays/flaskr/static/uploaded_files",
                                   post['brand_icon_name']))
            icon_name = str(datetime.datetime.now()) + '@' + pic0.filename
            pic0.save(os.path.join("/var/www/hongyuan_displays/flaskr/static/uploaded_files",
                                   icon_name))
        if not brand_name:
            error = 'Brand name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                ' UPDATE brands SET brand_name = ?, brand_icon_name = ? '
                ' WHERE brand_name = ?',
                (new_brand_name, icon_name, brand_name,)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('brand/brand_update.html', post=post)


@bp.route('/<string:brand_name>/brand_delete', methods=('POST',))
@login_required
def brand_delete(brand_name):
    db = get_db()

    post = db.execute(
        ' SELECT brand_name, brand_icon_name'
        ' FROM brands'
        ' WHERE brand_name = ?',
        (brand_name,)
    ).fetchone()

    os.remove(os.path.join("/var/www/hongyuan_displays/flaskr/static/uploaded_files",
                           post['brand_icon_name']))

    db.execute('DELETE FROM brands WHERE brand_name = ?', (brand_name,))
    db.commit()
    return redirect(url_for('log.index'))

@bp.route('/brand_search', methods=('GET', 'POST'))
def brand_search():
    if request.method == 'POST':
        search_key = json.loads(request.values.get("search_key"))

    posts = get_post(search_key)
    dicts = []
    for result in posts:
        dicts.append(dict(result))

    return json.dumps(dicts)

@bp.route('/get_all_brand_objs', methods=('GET', 'POST'))
def get_all_brand_objs():
    db = get_db()
    cats = db.execute(
        ' SELECT *'
        ' FROM brands'
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
        ' SELECT p.id, product_name, description, created, pic_name0, category, brand'
        ' FROM product p JOIN brands b ON p.brand = b.brand_name'
        ' WHERE brand_name == ?'
        ' ORDER BY created DESC',
        (key,)
    ).fetchall()

    if posts is None:
        abort(404, f"Post id {id} doesn't exist.")

    return posts
