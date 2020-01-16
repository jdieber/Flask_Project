## Our Routing file including all accassable pages

from app import app, db, login_manager, models, bcrypt
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required
from app.input import LoginForm, SignupForm
from app.models import User, City
import requests
from crypto_news_api import CryptoControlAPI
from bs4 import BeautifulSoup as bs
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
import os
import sys
import requests
import urllib.request

###################### Start Page ######################

@app.route('/index')
def index():
    user = {'username': 'Michael'}

    bar =   [ #moving news bar
        {
            'body': 'Still waters run deep'
        }
    ]
    return render_template('index.html', title='Home', user=user, bar=bar) #converts template into HTML page


###################### Login ######################

@app.route("/login", methods=['GET', 'POST']) # define the routes of our login page
@app.route("/", methods=['GET', 'POST']) # make it also accessable with only a slash
def login():
    # create an object of the login form
    form = LoginForm() #from the input file
    if request.method == "POST":
        username = request.form['username'] #s tore user input in username variable
        password = request.form['password'] # store user input in password variable

        user = User.query.filter_by(username=username).first() #Query the database

        # If the form validates correctly
        if form.validate_on_submit():
            if user is None: # check whether user exists in db
                flash("The username doesn't exist in the database") # if not, tell the user that he hasn't created an account yet
                return redirect(url_for('login'))
            else:
                if bcrypt.check_password_hash(user.password, password) is False:
                    flash("Wrong Password! Please try again.")
                    return redirect(url_for('login'))
                else:
                    login_user(user)
                    flash('Logged in user {}'.format(form.username.data))
                    return redirect(url_for('index'))
    return render_template('login.html', title="Login", form=form) # converts template into HTML page


###################### Logout ######################

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


###################### Signup ######################

#create route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    #create an object of the signup form
    form = SignupForm() #from the input file
    if request.method == "POST":
        # Retrieve input values from the form input fields
        username = request.form['username'] #again create a username variable
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8') #and a password variable
        test_password = request.form['test_password'] #for registration, we want to make sure that the pw was inputed without a typo, therefore the pw confirmation

        if form.validate_on_submit():
        # Check if the username is already taken. If True, redirect back
            if User.query.filter_by(username=username).first() is not None :
                flash('That username already exists. Please choose another username.') #let the user know that the desired username is not available anymore
                return redirect(url_for('signup')) #redirect to signup

            new_user = User(username, password) #input for the database
            db.session.add(new_user) #changes to your db. In this case we add the new user
            db.session.commit() #commit all changes

            #after the commit, we redirect the user back to the login page where he can login to our site for the first time
            flash('Account created. You can now log into the system.') #show him that the signup was successful
            return redirect(url_for('login')) #return the new signed up user to the login page so he/she can log in

    return render_template('signup.html', title="Sign Up", form=form) #converts template into HTML page


###################### Weather Page ######################

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        new_city= request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=b2a0213d9b0e1e919447e7ea59b2450d'

    weather_data =[]

    for city in cities:
        r = requests.get(url.format(city.name)).json() #response

        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)


###################### News API ######################

#user loader is registered with Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #convert the string id to int as our db needs numeric values


@app.route('/news' ,methods=['GET', 'POST'])
def news():
    api = CryptoControlAPI("46af633bdcb9d4ad4772ded65505727c") #get the API key from the CryptoCompare website
    top_news_raw = api.getTopNewsByCoin('bitcoin')
    x = (top_news_raw[0]['title'])
    y = (top_news_raw[1]['title'])
    z = (top_news_raw[2]['title'])
    return render_template('news.html', x=x, y=y, z=z)


###################### Meme - Scraper ######################

@app.route('/scraper')
def scraper():
    url = 'https://cheezburger.com/2160645/21-funniest-memes-of-the-day'
    r = requests.get(url)
    html = r.text
    soup = bs(html, 'lxml')

    data = soup.find_all("div", {"class": "resp-media-wrap"})

    links = []
    for a in soup.find_all("div", {"class": "resp-media-wrap"}):
        if a.img:
            links.append(a.img['data-src'])

    meme = links[0]
    return render_template('meme.html', meme=meme)
