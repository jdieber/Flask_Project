import os

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'no-one-will-never-guess'
