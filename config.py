import os

basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv

class Config:
    load_dotenv()

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
