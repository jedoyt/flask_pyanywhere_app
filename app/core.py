from flask import Blueprint, redirect, render_template, request, url_for

bp = Blueprint('core', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')