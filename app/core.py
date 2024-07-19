from flask import Blueprint, redirect, render_template, request, url_for

bp = Blueprint('core', __name__)

@bp.route('/')
def index():
    return render_template('index.html')