from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from app.settings import settings

metadata = MetaData(schema=settings.DB.SCHEMA)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()


def init_db(app: Flask):

    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB.DSN
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    migrate.init_app(app, db)
