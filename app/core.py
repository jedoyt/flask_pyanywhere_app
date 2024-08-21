from flask import Blueprint, redirect, render_template, request, url_for
from app.db import get_db

bp = Blueprint('core', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, content, created, user_id, full_name'
        ' FROM post p JOIN user u ON p.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('index.html', posts=posts)

@bp.route('/<int:id>/user_page', methods=('GET', 'POST'))
def user_page(id):
    return render_template('jaupy_blogs/user_profile.html')

@bp.route('/about')
def about():
    return render_template('about.html')