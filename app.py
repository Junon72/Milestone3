import os
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, url_for, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from config import Config 
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__, 
            template_folder="templates") 

app.config.from_object(Config)
toolbar = DebugToolbarExtension(app)    


mongo = PyMongo(app)

# Collections

users_collection = mongo.db.users
classes_collection = mongo.db.classes
series_collection = mongo.db.series
#array = list(users_collection.find())
#print(array)


@app.route('/')

# Login
@app.route('/index', methods=['GET'])
def index():
	# Check if user is logged in already
	if 'user' in session:
		user_in_db = users_collection.find_one({"username": session['user']})
		if user_in_db:
			# If in session redirect user to his/her collection of classes/ home page
			flash("You are logged in already!")
			return redirect(url_for('classes', user = user_in_db['username']))
	else:
		# Render the page for user to be able to log in
		return render_template("index.html", title = "Login", current_users = list(users_collection.find()))

# Check user login details from login form
@app.route('/user_auth', methods=['POST'])
def user_auth():
	form = request.form.to_dict()
	print('this form')
	print(form)
	user_in_db = users_collection.find_one({'username': form['username']})
	print('this user')
	print(user_in_db)
	# Check for user in database
	if user_in_db:
		# If passwords match (hashed / real password)
		if check_password_hash(user_in_db['password'], form['password']):
			print('this is not see')
			# Log user in (add to session)
			session['user'] = form['username']
			print('this session user')
			print(session['user'])
			return redirect(url_for('classes', username=user_in_db['username']))
			
		else:
			flash("Wrong password or user name!")
			print('oops!')
			return redirect(url_for('index'))
	else:
		flash("You must be registered!")
		return redirect(url_for('register'))

# Sign up
@app.route('/register', methods=['GET', 'POST'])
def register():
	# Check if user is not logged in already
	if 'user' in session:
		flash('You are already signed in!')
		return redirect(url_for('classes'))
	if request.method == 'POST':
		form = request.form.to_dict()
		# Check if the password1 and password2 actually match 
		if form['password'] == form['password']:
			# If matched find the user in db
			user = users_collection.find_one({"username" : form['username']})
			if user:
				flash(f"{form['username']} already exists!")
				return redirect(url_for('register'))
			# If user does not exist register new user
			else:				
				# Hash password
				hash_pass = generate_password_hash(form['password'])
				#Create new user with hashed password
				users_collection.insert_one(
					{
						'username': form['username'],
						'email': form['email'],
						'password': hash_pass
					}
				)
				# Check if user is actually saved
				user_in_db = users_collection.find_one({"username": form['username']})
				if user_in_db:
					# Log user in (add to session)
					session['user'] = user_in_db['username']
					return redirect(url_for('/index', user=user_in_db['username']))
				else:
					flash("There was a problem registering you, please try again")
					return redirect(url_for('register'))

		else:
			flash("The passwords are not identical!")
			return redirect(url_for('register'))
		
	return render_template(url_for('register'), title='Register')

# Log out
@app.route('/logout')
def logout():
	# Clear the session
	session.clear()
	flash('You were logged out!')
	return redirect(url_for('index'))

@app.route('/classes')           
def classes():          
    # Check if user is logged in
    if 'user' in session:
        # If so get the user classes and pass them to a template
        user_in_db = users_collection.find_one({'username': session['user']})
        username = session['user']
        # print(user)
        classes = classes_collection.find({'username': username})
        # print(classes)
        return render_template('classes.html',
                               title = 'Classes', 
                               username = username, 
                               classes = classes)
    else:
    	flash("You must be logged in!")
    	return redirect(url_for('index'))
 
############################### 
### Handling Classes / CRUD ###

# VIEW CLASS
@app.route('/view_class/<class_id>')
def view_class(class_id):
    this_class = classes_collection.find_one({'_id': ObjectId(class_id)})
    class_id = class_id
    print(this_class)
    print(class_id)
    return render_template('viewClass.html', 
                               title = 'Class',
                               class_id = class_id,  
                               this_class = this_class)

# ADD CLASS
@app.route('/add_class')
def add_class():
    username = session['user']
    user_id = users_collection.find_one({'username': session['user']})
    print(user_id)
    series = series_collection.find({'username': username})
    print(series)
    return render_template('addClass.html', title="New Class", 
                           user_id = user_id, username = username, series = series)

# insert() CLASS FROM save COMES HERE
@app.route('/insert_class', methods=['POST'])
def insert_class():
    username = session['user']
    print(username)
    new_class = {'class_name': request.form.get('class_name'),
                 'class_description': request.form.get('class_description'),
                 'main_elements': request.form.get('main_elements'),
                 'other_elements': request.form.get('other_elements'),
                 'playlist_title': request.form.get('playlist_title'),
                 'playlist_link': request.form.get('playlist_link'),
                 'series': [],
                 'class_notes': request.form.get('class_notes'),
                 'exercises': [],
                 'logs': [],
                 'user_id': request.form.get('user_id'),
                 'username': request.form.get('username')}
    
    print(new_class)
    inserted_class = classes_collection.insert_one(new_class)
    print(inserted_class)
    this_class = inserted_class
    class_id = inserted_class.inserted_id
    print(class_id)
    series = request.form.getlist('series')
    print(series)
    classes_collection.update(
        {'_id': ObjectId(class_id)},
        { '$set': { 'series': series}})
	
    return redirect(url_for('view_class', class_id=class_id, username=username, this_class=this_class ))

# EDIT CLASS
@app.route('/edit_class/<class_id>')
def edit_class(class_id):
    username = session['user']
    user_data = users_collection.find_one({'username': session['user']})
    this_class =  classes_collection.find({"_id": ObjectId(class_id)})
    print(this_class)
    class_id = class_id
    print(class_id)
    series = series_collection.find({'username': username})
    print(series)
    return render_template('editClass.html', title="Edit Class", this_class = this_class, class_id = class_id, series = series)


# save() CLASS COMES HERE -> 
@app.route('/save_class')
def save_class():
    
    print("Class was saved")
    return redirect(url_for('view_class'))

# DELETE CLASS - remove() -> to view
@app.route('/delete_class/<class_id>')
def delete_class(class_id):
    deleted_class = classes_collection.remove({'_id': ObjectId(class_id)})
    print(deleted_class)
    return redirect(url_for('classes',
                               title = 'Classes'))

# DUPLICATE CLASS -> to form
@app.route('/copy_class')
def copy_class():
    print("Class was duplicated")
    return redirect(url_for('save_class', title="Edit Class(copy)"))
    # Get the class and populate the form with some additional information - add (copy) in name value 

##########################
## Handling Logs / CRUD ##

# ADD LOG
@app.route('/add_log/<class_id>')
def add_log(class_id):
    print(class_id)
    return render_template('addLog.html')
                 
# save() log
@app.route('/insert_log/<class_id>', methods=['POST'])
def insert_log(class_id):
    new_log = {
        'log_date': request.form.get('log_date'),
        'log_text': request.form.get('log_text'),
        'log_tag': request.form.get('log_tag')  
	}
    
    inserted_log = classes_collection.save({_id: ObjectId(class_id)}, { '$push': {new_log}})
    log_id = inserted_log.inserted_id
    print(log_id)
    return redirect(url_for('editClass', title='Edit Class', log_id = log_id, class_id = class_id))

# DELETE LOG - $pull{}
@app.route('/delete_log/<class_id>/<log_id>')           
def delete_log(class_id, log_id):
    deleted_log = classes_collection.update({'_id': ObjectId(class_id)}, {'$pull': {'_id': ObjectId(log_id)}} )
    print(deleted_log)
    return redirect(url_for('editClass', title='Edit Class'))

#################################
### Handling Exercises / CRUD ###

# ADD EXERCISE
@app.route('/add_exercise/<class_id>')
def add_exercise(class_id):
    this_class =  classes_collection.find_one({"_id": ObjectId(class_id)})
    print("Exercise was added")
    return render_template('addExercise.html', title='New exercise', this_class = this_class, class_id=class_id)

# insert() exercise
# @app.route('/insert_exercise/<class_id>')
# def insert_exercise(class_id):
    # print("Exercise was inserted")
    # return redirect(url_for('edit_class', class_id=class_id))

# EDIT EXERCISE
@app.route('/edit_exercise', methods=['GET', 'POST'])
def edit_exercise():
    print('Exercise was edited')
    return render_template(url_for('editExercise'), title='Edit exercise')

# update() EXERCISE COMES HERE
@app.route('/update_exercise', methods=['POST'])
def update_exercise():
	print("Exercise was updated")
	return redirect(url_for('edit_class'))

# DELETE EXERCISE
@app.route('/delete_exercise')
def delete_exercise():
    print("Exercise was deleted")
    return redirect(url_for('editClass'), title='Edit Class')

####################################
### Handling Music Tracks / CRUD ###

 # ADD MUSIC TRACK
@app.route('/add_track/<class_id>/<exercise_id>', methods=['POST'])
def add_track(class_id, exercise_id):
    print(class_id)
    print(exercise_id)
    return render_template(url_for('addTrack'), title="Music Track", class_id = class_id, exercise_id = exercise_id)

# save() track
@app.route('/insert_track/<class_id>/<exercise_id>', methods=['POST'])
def insert_track(class_id, exercise_id):
    new_track = {
        'track_title': request.form.get('track_title'),
        'track_link': request.form.get('track_link'),
        'track_comment': request.form.get('track_comment')
	}
    inserted_track = classes_collection.save({_id: ObjectId(class_id)}, { 'exercises' :{ '$push': {new_track}}})
    track_id = inserted_track.inserted_id
    print(track_id)
    return redirect(url_for('edit_exercise'), title='Edit Exercise')

# DELETE MUSIC  TRACK- $pull{} 
@app.route('/delete_track/<class_id>/<exercise_id>')
def delete_track(class_id, exercise_id):
    deleted_track = classes_collection.update({'_id': ObjectId(class_id)}, {'$pull': { 'exercises' : {'_id': ObjectId(log_id)}} })
    print("Track was deleted")
    return redirect(url_for('editExercise'), title='Edit Exercise')

####################################
### Handling Video Links / CRUD ###

# ADD VIDEO LINK
@app.route('/add_link', methods=['POST'])
def add_link():
    print("Link was added")
    return render_template(url_for('addLog'))

# insert() link
@app.route('/insert_link', methods=['POST'])
def insert_link():
    print("Link was inserted")
    return redirect(url_for('edit_exercise'), title='Edit Exercise')

# DELETE MUSIC - remove()
@app.route('/delete_link')
def delete_link():
    print("Link was deleted")
    return redirect(url_for('edit_exercise'), title='Edit Exercise')

####################################
### Handling Class Series / CRUD ###

# VIEW CLASS SERIES
@app.route('/series')           
def series():
    # Check if user is logged in
    if 'user' in session:
        # If so get the user classes and pass them to a template
        user_in_db = users_collection.find_one({'username': session['user']})
        username = session['user']
        series = series_collection.find({'username': username})
        print(series)
        print(username)
        print(user_in_db)
        return render_template('series.html',
                               title = 'Series', 
                               username = username,
                               series = series)
    else:
    	flash("You must be logged in!")
    	return redirect(url_for('index'))
           

# VIEW CLASSES IN SERIES

@app.route('/view_classes_in_series')           
def view_classes_in_series(): 
    print("Classes in series view opened")            
    return render_template('classes.html')

# ADD CLASS SERIES
@app.route('/add_series')
def add_series():
    username = session['user']
    user_id = users_collection.find_one({'username': session['user']}, {'_id': 1})
    print(user_id)
    # This checks if the user already has a document in series collection, if not a document will be added.
    # https://stackoverflow.com/questions/25163658/mongodb-return-true-if-document-exists: answer by Xavier Guihot led to the right path with this.
    if series_collection.count_documents({'username': session['user']}, limit = 1) ==0:
        user_series_set = {
            'user_id': user_id,
            'username': username,
            'classes': []
            }
        
        inserted_set = series_collection.insert_one(user_series_set)
        doc = inserted_set.inserted_id
        print(doc)
    return render_template('addSeries.html', title="Add Series", user_id = user_id, username = username)

# insert() series/ update_one() in class_series []
@app.route('/insert_series', methods=['POST'])
def insert_series():
    
    username = session['user']
    print(username)
    new_series = {
        '_id': ObjectId(),
        'series_name': request.form.get('series_name'),
        'series_description': request.form.get('series_description'),
        'class_series': []
        }
    
    # Check if the series name already exist.
    series = series_collection.find_one({"series_name" : form['series_name']})
    if series:
        flash(f"{form['series_name']} already exists! Give the series a unique name.")
        return redirect(url_for('add_series'))
                                
    inserted_series = series_collection.update_one({'username': username}, { '$addToSet' :{ 'class_series':new_series}})
    print(inserted_series)
    return redirect(url_for('series', title='Series', username=username ))

# EDIT SERIES
@app.route('/edit_series/<series_doc>/<series_id>')
def edit_series(series_doc, series_id):
    username = session['user']
    this_series = series_collection.find_one({'username': username})
    print(this_series)
    return render_template('editSeries.html', title='Edit series')

# update() SERIES COMES HERE
@app.route('/update_series/<series_doc>/<series_id>', methods=['POST'])
def update_series(series_doc, series_id):
    print(series_doc, series_id)
    return redirect(url_for('series'))

# DELETE CLASS SERIES - remove()
@app.route('/delete_series/<series_doc>/<series_id>')
def delete_series(series_doc, series_id):
    deleted_series = series_collection.update_one({'_id': ObjectId(series_doc)}, { '$pull' : { 'class_series' : {'_id': ObjectId(series_id)}}} )
    print(deleted_series)
    return redirect(url_for('series'))


if __name__ == '__main__': 

   app.run(host=os.environ.get('IP'),             
                                                  
      port=int(os.environ.get('PORT', 5000)),
      debug=True)           