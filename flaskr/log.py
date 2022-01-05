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


@bp.route('/product_create', methods=('GET', 'POST'))
@login_required
def product_create():
    if request.method == 'POST':
        product_name = request.form['product_name']
        description = request.form['description']
        cat = request.form['cat']
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
                'INSERT INTO product (product_name, description, author_id, pic_name0, pic_name1, pic_name2, category, recommend, accessories)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (product_name, description, g.user['id'], pic_name0, pic_name1, pic_name2, cat, rec, acc)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('log/product_create.html')


@bp.route('/cat_create', methods=('GET', 'POST'))
@login_required
def cat_create():
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        error = None

        if not cat_name:
            error = 'Category name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO category (cat_name)'
                ' VALUES (?)',
                (cat_name,)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('log/cat_create.html')


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


@bp.route('/<int:id>/product_update', methods=('GET', 'POST'))
@login_required
def product_update(id):
    post = get_post(id)
    pic_name0 = post['pic_name0']
    pic_name1 = post['pic_name1']
    pic_name2 = post['pic_name2']

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        cat = request.form['cat']
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
                'UPDATE product SET product_name = ?, description= ?, category= ?, recommend= ?, accessories= ?, pic_name0= ?, pic_name1= ?, pic_name2= ?'
                ' WHERE id = ?',
                (title, body, cat, rec, acc, pic_name0, pic_name1, pic_name2, id)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('log/product_update.html', post=post)


@bp.route('/<int:id>/product_delete', methods=('POST',))
@login_required
def product_delete(id):
    post = get_post(id)
    os.remove(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files", post['pic_name0']))
    os.remove(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files", post['pic_name1']))
    os.remove(os.path.join("/Users/zhangjing/Documents/GitHub/hongyuan_displays/flaskr/static/uploaded_files", post['pic_name2']))

    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('log.index'))


@bp.route('/<string:cat_name>/cat_update', methods=('GET', 'POST'))
@login_required
def cat_update(cat_name):
    post = get_db().execute(
        ' SELECT cat_name'
        ' FROM category'
        ' WHERE cat_name = ?',
        (cat_name,)
    ).fetchone()

    if request.method == 'POST':
        new_cat_name = request.form['cat_name']
        error = None

        if not cat_name:
            error = 'Category name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                ' UPDATE category SET cat_name = ?'
                ' WHERE cat_name = ?',
                (new_cat_name, cat_name,)
            )
            db.commit()
            return redirect(url_for('log.index'))

    return render_template('log/cat_update.html', post=post)


@bp.route('/<string:cat_name>/cat_delete', methods=('POST',))
@login_required
def cat_delete(cat_name):
    db = get_db()
    db.execute('DELETE FROM category WHERE cat_name = ?', (cat_name,))
    db.commit()
    return redirect(url_for('log.index'))
