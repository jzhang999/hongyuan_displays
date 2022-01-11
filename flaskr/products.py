import os
import datetime

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
        'SELECT p.id, product_name, description, created, author_id, username, pic_name0, pic_name1, pic_name2, accessories'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('products/index.html', posts=posts)

@bp.route('/product_create', methods=('GET', 'POST'))
@login_required
def product_create():
    if request.method == 'POST':
        product_name = request.form['product_name']
        description = request.form['description']
        cat = request.form['cat']
        brand = request.form['brand']
        rec = request.form['rec']
        acc = request.form['acc']

        # for saving the pics
        pic0 = request.files['file0']
        pic_name0 = str(datetime.datetime.now()) + '@' + pic0.filename
        pic0.save(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files", pic_name0))

        pic1 = request.files['file1']
        pic_name1 = str(datetime.datetime.now()) + '@' + pic1.filename
        pic1.save(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files", pic_name1))

        pic2 = request.files['file2']
        pic_name2 = str(datetime.datetime.now()) + '@' + pic2.filename
        pic2.save(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files", pic_name2))

        error = None

        if not product_name:
            error = 'Product name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (product_name, description, author_id, pic_name0, pic_name1, pic_name2, category, brand, recommend, accessories)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (product_name, description, g.user['id'], pic_name0, pic_name1, pic_name2, cat, brand, rec, acc)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('products/product_create.html')

@bp.route('/<int:id>/product_update', methods=('GET', 'POST'))
@login_required
def product_update(id):
    post = get_post_web(id)
    pic_name0 = post['pic_name0']
    pic_name1 = post['pic_name1']
    pic_name2 = post['pic_name2']

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        cat = request.form['cat']
        br = request.form['br']
        rec = request.form['rec']
        acc = request.form['acc']
        pic0 = request.files['file0']
        pic1 = request.files['file1']
        pic2 = request.files['file2']

        error = None

        # see if the pic is changed
        if pic0.filename != "":
            os.remove(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files",
                                   post['pic_name0']))
            pic_name0 = str(datetime.datetime.now()) + '@' + pic0.filename
            pic0.save(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files",
                                   pic_name0))

        if pic1.filename != "":
            os.remove(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files",
                                   post['pic_name1']))
            pic_name1 = str(datetime.datetime.now()) + '@' + pic1.filename
            pic1.save(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files",
                                   pic_name1))

        if pic2.filename != "":
            os.remove(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files",
                                   post['pic_name2']))
            pic_name2 = str(datetime.datetime.now()) + '@' + pic2.filename
            pic2.save(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files",
                                   pic_name2))

        if not title:
            error = 'Product name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET product_name = ?, description= ?, category= ?, brand= ?, recommend= ?, accessories= ?, pic_name0= ?, pic_name1= ?, pic_name2= ?'
                ' WHERE id = ?',
                (title, body, cat, br, rec, acc, pic_name0, pic_name1, pic_name2, id)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('products/product_update.html', post=post)

@bp.route('/<int:id>/product_delete', methods=('POST',))
@login_required
def product_delete(id):
    post = get_post_web(id)
    os.remove(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files", post['pic_name0']))
    os.remove(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files", post['pic_name1']))
    os.remove(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files", post['pic_name2']))

    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('log.index'))

@bp.route('/product_search', methods=('GET', 'POST'))
def product_search():
    if request.method == 'POST':
        search_key = json.loads(request.values.get("search_key"))
        key = search_key["input"]

    posts = get_post_app(key)
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

def get_post_web(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, product_name, description, created, author_id, username, category, brand, recommend, pic_name0, pic_name1, pic_name2, accessories'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

def get_post_app(key):
    posts = get_db().execute(
        ' SELECT p.id, product_name, description, created, pic_name0, category'
        ' FROM product p'
        ' WHERE product_name LIKE ?',
        ('%'+key+'%',)
    ).fetchall()

    if posts is None:
        abort(404, f"Post id {id} doesn't exist.")

    return posts


def get_post_id(id):
    posts = get_db().execute(
        ' SELECT p.id, product_name, description, created, pic_name0, pic_name1, pic_name2, category'
        ' FROM product p'
        ' WHERE id == ?',
        (id,)
    ).fetchall()

    if posts is None:
        abort(404, f"Post id {id} doesn't exist.")

    return posts


def get_post_rec():
    posts = get_db().execute(
        ' SELECT p.id, product_name, description, created, pic_name0, category'
        ' FROM product p'
        ' WHERE recommend == "是"'
    ).fetchall()

    if posts is None:
        abort(404, f"Post id {id} doesn't exist.")

    return posts