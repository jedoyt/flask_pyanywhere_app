import functools, re

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not valid_username(username=username):
            error = "Invalid username!\nUse only characters from 'a-z', 'A-Z', '0-9', and '_' (underscore).\nNo space(s) allowed."
            session['registration_error'] = error
            return render_template(
                'jaupy_blogs/auth/register.html', error=session['registration_error']
                )
        elif not password:
            error = 'Password is required.'

        try:
            db.execute(
                "INSERT INTO user (username, email, password, full_name)"
                " VALUES (?, ?, ?, ?)", (username, email, generate_password_hash(password), full_name)
            )
            db.commit()
        except db.IntegrityError:
            error = "username or email is already registered."
            session['registration_error'] = error
            return render_template(
                'jaupy_blogs/auth/register.html', error=session['registration_error']
                )
        else:
            return redirect(url_for('auth.login'))

    return render_template('jaupy_blogs/auth/register.html')

def valid_username(username):
    pattern = "^[a-zA-Z0-9_]+$"
    if re.match(pattern, username):
        return True
    else:
        return False

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect Email or password'
            session['login_error'] = error
            return render_template('jaupy_blogs/auth/login.html', error=session['login_error'])
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect Email or password'
            session['login_error'] = error
            return render_template('jaupy_blogs/auth/login.html', error=session['login_error'])
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('core.index'))
        flash(error)
        
    return render_template('jaupy_blogs/auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('core.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view