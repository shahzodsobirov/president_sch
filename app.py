from flask import Flask, render_template, request
from backend.models.basics_models import *

app = Flask(__name__)

app.config.from_object('backend.models.config')
db = db_setup(app)
migrate = Migrate(app, db)

from backend.user.views import *
from backend.basics.views import *

if __name__ == '__main__':
    app.run()

