## This is our user database model

from app import app, db
from flask_login import UserMixin

## Create a model for the table structure in the dataabse
class User(db.Model, UserMixin):

    __tablename__ = 'flaskappusers'
    ## ID as primary key, unique username, password
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(400), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '' % self.username

####### WEATHER #######

class City(db.Model):

    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
