# Import flask deps
from app import app, db, config
from flask import Blueprint, request, render_template, flash, g, session, \
        redirect, url_for

location_list = config.keys()
print(location_list)

@app.route("/<location>/")
def home(location):
    print(location)
    if location in location_list:
        print(location)
        return render_template("m01_homepage/home.html", location=location, config=config[location])
    else:
        return "Not a valid location"


