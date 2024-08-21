from datetime import datetime
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort, NotFound, Forbidden

from app.auth import login_required
from app.db import get_db


bp = Blueprint('blog', __name__)


@bp.route('/compose_blog', methods=('GET', 'POST'))
@login_required
def compose_blog():
    if request.method == 'POST':
        created = datetime.now()
        title = request.form['title']
        content = request.form['content']
        error = None

        if not content:
            error = 'Content is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (created, title, content, user_id)'
                ' VALUES (?, ?, ?, ?)', (created, title, content, g.user['id'])
            )
            db.commit()
            return redirect(url_for('core.index'))
        
    return render_template('jaupy_blogs/compose_blog.html')

def get_post(id, check_user=True):
    post = get_db().execute(
        'SELECT p.id, title, content, user_id, username'
        ' FROM post p JOIN user u ON p.user_id = u.id'
        ' WHERE p.id = ?;', (id,)
    ).fetchone()

    if post is None:
        raise NotFound
    if check_user and post['user_id'] != g.user['id']:
        raise Forbidden
    return post

@bp.route('/<int:id>/edit_blog', methods=('GET', 'POST'))
@login_required
def edit_blog(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = None
        
        if not content:
            error = 'Content is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, content = ?'
                ' WHERE id = ?', (title, content, id)
            )
            db.commit()
            return redirect(url_for('core.index'))
    return render_template('jaupy_blogs/edit_blog.html', post=post)

@bp.route('/<int:id>/delete_blog', methods=('GET', 'POST'))
@login_required
def delete_blog(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('core.index'))