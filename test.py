### test.py file was used to create tests for the installation of python and python modules ##

## Test for python installation, version and the path ##
# import sys

# this line prints if python is installed correctly
# def greet(greetings_to):
  # greeting = 'Hello, {}'.format(greetings_to)
  # return greeting
 
# print(greet('World!'))

# this line will print out the current python path and the version of the python
# print(sys.executable)

## Test for running Flask in VSCode ##
# Functionalities to import from modules
import os                  # Imports operating system dependent functionality.
from flask import Flask    # Imports Flask class from flask module .

app = Flask(__name__)      # An instance of Flask class construction.

# Route Decorator
@app.route('/')            # URL handled by main() route handler.
                        
def welcome():             # Defines a  function that returns "Hello World".
    return "Welcome Flask!"
if __name__ == '__main__': # the global namespace __name__ is set to equal "__main__"

# If conditional statement is satisfied
   app.run(host=os.environ.get('IP'),             # launches the Flask built-in development web server and   
                                                   # gets the IP Address from the operating system.
      port=int(os.environ.get('PORT', 8080)),# gets PORT we want to open, which in this case is set to 5000.
      debug=True)                            # To enable reloader and debugger by setting it to True, 
                                                   # which is the recommended value for the development phase

# import os                  
import pymongo
from pymongo import MongoClient
# from flask import Flask, render_template, redirect, request, url_for
from config import Config
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__) 
app.config.from_object(Config)     

# MongoDB name
# app.config['MONGO_DBNAME'] = 'classapp'
# MongoDB URI / Assign db
# client = MongoClient(Config.MONGO_URI)
# db = client.classapp


mongo = PyMongo(app)

# MONGO CONNECTION TEST
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print('Could not connect to MongoDB: %s') % e

conn = mongo_connect(MONGO_URI)