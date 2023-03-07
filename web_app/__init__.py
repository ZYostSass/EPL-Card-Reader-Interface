import os

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:///project.db"
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import init_db

    init_db(app)

    from . import models
    from . import views

    app.register_blueprint(views.bp)

    from . import admin

    app.register_blueprint(admin.bp)


    return app
