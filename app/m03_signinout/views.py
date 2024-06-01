# Import flask deps
from app import app, db, config
from flask import Blueprint, request, render_template, flash, g, session, \
        redirect, url_for

class Sign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initial = db.Column(db.String(1), nullable=False)
    surname = db.Column(db.String(), nullable=True)
    timestamp = db.Column(db.DateTime(), nullable=False)
    sign_in = db.Column(db.Boolean(), nullable=False)

location_list = config.keys()

@app.route("/<location>/signinout")
def signinout(location):
    if location in location_list:
        return render_template("m03_signinout/index.html", config=config[location], location=location)
    else:
        return "Not a valid location"

@app.route("/sign_submit", methods=['POST'])
def sign():
    fn = request.form["fn"]
    ln = request.form["ln"]
    sign = request.form["sign_type"]

    print(fn, ln, sign)

    return '', 204