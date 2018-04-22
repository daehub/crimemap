#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Daehub'

from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import json


app = Flask(__name__)
DB = DBHelper()


@app.route('/')
def home():
    try:
        # data = DB.get_all_inputs()
        crimes = DB.get_all_crimes()
        crimes = json.dump(crimes)
    except Exception as e:
        print(e)
        # data = None
    return render_template('home.html',crimes=crimes)


@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print(e)
    return home()


@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()


@app.route("/submitcrime", methods=["POST"])
def submitcrime():
    try:
        category = request.form.get("category")
        date = request.form.get("date")
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
        description = request.form.get("description")
        DB.add_crime(category,date,latitude,longitude,description)
    except Exception as e:
        print(e)
    return home()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
