from flask import Blueprint, redirect, render_template, request, url_for, session
from app.db import get_db
from werkzeug.exceptions import Unauthorized

bp = Blueprint('core', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, content, created, user_id, full_name'
        ' FROM post p JOIN user u ON p.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    # Paginate Blogs
    page = request.args.get('page', 1, type=int)
    per_page = 5
    paginated_results = paginate_results(results=posts, page=page, per_page=per_page)
    total_pages = len(posts) // per_page + (len(posts) % per_page > 0)

    return render_template('index.html', posts=paginated_results, total_pages=total_pages, current_page=page)

def paginate_results(results, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return results[start:end]

@bp.route('/<int:id>/user_page', methods=('GET', 'POST'))
def user_page(id):
    if session['user_id'] != id:
        raise Unauthorized
    user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (id,)
    ).fetchone()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        full_name = request.form['full_name']

        db = get_db()
        db.execute(
            'UPDATE user SET username = ?, email = ?, full_name = ? WHERE id = ?;',
            (username, email, full_name, session['user_id'])
            )
        db.commit()
        return redirect(url_for('core.user_page', id=session['user_id']))

    return render_template('jaupy_blogs/user_profile.html', user=user)

@bp.route('/about')
def about():
    return render_template('about.html')