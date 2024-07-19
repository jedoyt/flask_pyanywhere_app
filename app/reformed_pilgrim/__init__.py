from flask import render_template, Blueprint, request


bp = Blueprint('reformed_pilgrim', __name__)

@bp.route('/reformed_pilgrim', methods=['GET', 'POST'])
def index():
    return render_template('reformed_pilgrim/reformed_pilgrim_index.html')