from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

#app.config.from_object(Config)
app.config['SECRET_KEY'] = 'secretkeyvalue'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://h1630128:h1630128@balrog.wu.ac.at/h1630128'


bcrypt = Bcrypt(app) #encrypt

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app import routes, models

#db.metadata.clear()
db.create_all()
db.session.commit()
