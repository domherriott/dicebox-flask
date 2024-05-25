from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    minPlayers = db.Column(db.Integer, nullable=False)
    maxPlayers = db.Column(db.Integer, nullable=False)

class Category(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    high_level_category = db.Column(db.String(100), nullable=False, primary_key=True)

class Mechanic(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    high_level_mechanic = db.Column(db.String(100), nullable=False, primary_key=True)

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")




@main.route("/search")
def search():
    q = request.args.get("q")
    print(q)

    players = request.args.get("players")
    category = request.args.get("category")
    mechanic = request.args.get("mechanic")

    print(mechanic)
    print(players)


    if q and players and category and mechanic:
        results = Game.query \
            .join(Category, Game.id==Category.game_id)\
            .join(Mechanic, Game.id==Mechanic.game_id)\
            .filter(Game.id.icontains(q) | Game.title.icontains(q)) \
            .filter(Game.minPlayers <= players, Game.maxPlayers >= players) \
            .filter(Category.high_level_category == category) \
            .filter(Mechanic.high_level_mechanic == mechanic) \
            .order_by(Game.title.asc()).limit(100).all()
    elif q:
        results = Game.query \
            .filter(Game.id.icontains(q) | Game.title.icontains(q)) \
            .order_by(Game.title.asc()).limit(100).all()
    elif players:
        results = Game.query \
            .filter(Game.minPlayers <= players, Game.maxPlayers >= players) \
            .order_by(Game.title.asc()).limit(100).all()
    else:
        results = Game.query \
            .order_by(Game.title.asc()).limit(100).all()

    return render_template("search_results.html", results=results)

def load_data():
    db.drop_all()
    db.create_all()
    # print(db.tables)
    df = pd.read_csv("./bgg_export.csv")

    
    for index, row in df.iterrows():
        game = Game(
            id=row["objectid"],
            title=row["name"],
            minPlayers=row["min_players"],
            maxPlayers=row["max_players"]
        )
        db.session.add(game)
    
    df_cat = pd.read_csv("./bgg_export_cat.csv")

    for index, row in df_cat.iterrows():
        if row["high_level_category"] is not np.nan:
            category = Category(
                game_id=row["id"],
                high_level_category=row["high_level_category"],
            )
            db.session.add(category)

    df_mech = pd.read_csv("./bgg_export_mech.csv")

    for index, row in df_mech.iterrows():
        if row["high_level_mechanic"] is not np.nan:
            mechanic = Mechanic(
                game_id=row["id"],
                high_level_mechanic=row["high_level_mechanic"],
            )
            db.session.add(mechanic)

    db.session.commit() 

def create_app():

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    db.init_app(app)

    with app.app_context():
        load_data()
    app.register_blueprint(main)

    return app



