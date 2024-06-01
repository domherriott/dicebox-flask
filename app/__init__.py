from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np

db = SQLAlchemy()
main = Blueprint("main", __name__)




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db.init_app(app)

app.register_blueprint(main)

config = {
    'dicebox-peterborough':{
        'logo': 'images/dicebox.png',
        'color': '#47bfdf',
        'pages': ['gamelist', 'signinout']
    },

    'dicebox-stockport':{
        'logo': 'images/dom_and_kimi.jpeg',
        'color': '#df4791',
        'pages': ['signinout']
    }
}


# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Home page view
@app.route('/')
def root():
    return render_template('home.html')

from app.m01_homepage import views
from app.m02_gamelist import views
from app.m03_signinout import views