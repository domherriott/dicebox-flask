from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(), nullable=True)
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

@main.route("/load")
def load():
    results = Game.query.order_by(Game.title.asc()).limit(100).all()
    return render_template("search_results.html", results=results)


@main.route("/search")
def search():
    q = request.args.get("q")
    print(q)

    players = request.args.get("players")
    if players == "6+":
        min_players = 6
        max_players = 100
    else:
        min_players = players
        max_players = players

    category = request.args.get("category")
    mechanic = request.args.get("mechanic")

    print(mechanic)
    print(players)

    print(q, min_players, max_players, category, mechanic)

    results = Game.query
    
    if q:
        results = results.filter(Game.id.icontains(q) | Game.title.icontains(q))
    
    if players:
        results = results.filter(Game.minPlayers <= min_players, Game.maxPlayers >= max_players)

    if category:
        results = results.join(Category, Game.id==Category.game_id) \
            .filter(Category.high_level_category == category)
        
    if mechanic:
        results = results.join(Mechanic, Game.id==Mechanic.game_id) \
            .filter(Mechanic.high_level_mechanic == mechanic)
        
    results = results.order_by(Game.title.asc()).limit(100).all()

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
            thumbnail=row["thumbnail_x"],
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



