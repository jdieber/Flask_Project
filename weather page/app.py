import requests
from flask import flask, render_template
from flask_sqlalchemy import SQL Alchemy

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('weather.html')
