import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "this-is-a-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db' + os.path.join(basedir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False