#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Daehub'


import dateparser
import datetime
from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import json
import string

app = Flask(__name__)
DB = DBHelper()
Categories = ['mugging','break-in']

@app.route('/')
def home(error_message = None):
    try:
        # data = DB.get_all_inputs()
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
    except Exception as e:
        print(e)
        # data = None
    return render_template('home.html',crimes=crimes,categories = Categories,error_message = error_message)


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
def submitCrime():
    try:
        category = request.form.get("category")
        if category not in Categories:
            return home()
        date = format_date(request.form.get("date"))
        if not date:
            return home('Invalid date format! Please use yyyy-mm-dd')
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
        description = request.form.get("description")
        description = sanitize_string(description)
        DB.add_crime(category,date,latitude,longitude,description)
    except Exception as e:
        print(e)
    except ValueError:
        return home()
    return home()


def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date,"%Y-%d-%m")
    except TypeError:
        return None


def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + '''!?$,.;:-'( 
    )&"'''
    tmList = list (filter(lambda x: x in whitelist,userinput))
    result = ''.join(tmList)
    return result

if __name__ == '__main__':
    app.run(port=5000, debug=True)
