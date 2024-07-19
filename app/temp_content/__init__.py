from flask import Blueprint, render_template, request, url_for

bp = Blueprint('temp_content', __name__)

@bp.route('/temp_content')
def index():
    return render_template('temp_content/temp_content.html')