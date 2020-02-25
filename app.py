import os                  
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, url_for
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

@app.route('/')
@app.route('/home')           
def home():             
    return render_template('home.html', classes = mongo.db.classes.find({}, {"CLASSES.class_name": 1}))

@app.route('/about')           
def about():             
    return render_template('about.html', title='About')

@app.route('/get_classes')           
def get_classes():             
    return render_template('classes.html', title='Classes', classes = mongo.db.classes.find({}, {"CLASSES":1}))

@app.route('/series')           
def series():             
    return render_template('series.html', title='Series', series=series_data)


if __name__ == '__main__': 

   app.run(host=os.environ.get('IP'),             
                                                  
      port=int(os.environ.get('PORT', 5000)),
      debug=True)           