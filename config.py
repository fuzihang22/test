#From flask mega tutorial - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #Secret key used for generating CSRF tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False