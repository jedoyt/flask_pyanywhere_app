import os
from flask import Flask

app = Flask(__name__)

### DATABASE SETUP ###


### BLUEPRINT REGISTRATIONS ###
from . import core
app.register_blueprint(core.bp)

from . import flames_app
app.register_blueprint(flames_app.bp)

from . import reformed_pilgrim
app.register_blueprint(reformed_pilgrim.bp)

from . import temp_content
app.register_blueprint(temp_content.bp)