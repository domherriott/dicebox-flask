from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    minPlayers = db.Column(db.Integer, nullable=False)
    maxPlayers = db.Column(db.Integer, nullable=False)

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")




@main.route("/search")
def search():
    q = request.args.get("q")
    print(q)

    players = request.args.get("players")
    print(players)

    if q and players:
        results = Game.query \
            .filter(Game.id.icontains(q) | Game.title.icontains(q)) \
            .filter(Game.minPlayers <= players, Game.maxPlayers >= players) \
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
    df = pd.read_csv("./data/data.csv")

    
    for index, row in df.iterrows():
        game = Game(
            id=row["gameId"],
            title=row["name"],
            minPlayers=row["minPlayers"],
            maxPlayers=row["maxPlayers"]
        )
        db.session.add(game)
    

    db.session.commit() 

def create_app():

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    db.init_app(app)

    with app.app_context():
        load_data()
    app.register_blueprint(main)

    return app



