import os

from flask import Flask
from app.db import close_db, init_db_command, init_app

app = Flask(__name__)

### CONFIGS ###
# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
app.config['SECRET_KEY'] = 'dev'
app.config['DATABASE'] = os.path.join(app.instance_path, 'flask_app.sqlite')

init_app(app=app)
# app.teardown_appcontext(close_db)
# app.cli.add_command(init_db_command)

### BLUEPRINT REGISTRATIONS ###
from . import core
app.register_blueprint(core.bp)

from . import auth
app.register_blueprint(auth.bp)

from . import blog
app.register_blueprint(blog.bp)

from . import error_handlers
app.register_blueprint(error_handlers.bp)

from . import flames_app
app.register_blueprint(flames_app.bp)

from . import reformed_pilgrim
app.register_blueprint(reformed_pilgrim.bp)

from . import temp_content
app.register_blueprint(temp_content.bp)

from . import kjv_bible
app.register_blueprint(kjv_bible.bp)
