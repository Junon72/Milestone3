import os
import pymongo
import jinja2
import json
import re
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, url_for, session, flash
from config import Config
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder="templates")


# The general configuration, together with the db configuration are stored in config.py file
# The file is accessed using Python config module
app.config.from_object(Config)


mongo = PyMongo(app)

# Collections vars

users_collection = mongo.db.users
classes_collection = mongo.db.classes
series_collection = mongo.db.series


# Login/ Logout and Register functions

@app.route('/', methods=['GET'])
def index():
	''' Login function. The function first checks if user is added to the session already.
	If not the user is directed to the login form, otherwise the the classes view will be rendered. 
	'''
	if 'user' in session:
		user_in_db = users_collection.find_one({"username": session['user']})
		if user_in_db:
			# If in session redirect user to his/her collection of classes/ home page
			flash("You are logged in already!", "success")
			return redirect(url_for('classes', 
							username = user_in_db['username']))
	else:
		# Render the page for user to be able to log in
		return render_template("index.html", title = "Login", 
								current_users = list(users_collection.find()))


@app.route('/user_auth', methods=['POST'])
def user_auth():
	'''User authentication function checks the user filled details in login form 
	by finding the user in db users collection.
	If the user name is in db, the hashed password is checked.
	If the password matches the user is added to the session and directed to the classes page.
	If not the login form is rendered again. 
	If user is not found in db, the user is directed to the register page.
	'''
	form = request.form.to_dict()
	user_in_db = users_collection.find_one({'username' : form['username']})
	# Check for user in database
	if user_in_db:
		# If passwords match (hashed / real password)
		if check_password_hash(user_in_db['password'], form['password']):
			# Log user in (add to session)
			session['user'] = form['username']
			return redirect(url_for('classes', 
							username = user_in_db['username']))

		else:
			flash("Wrong password or user name!", "warning")
			return redirect(url_for('index'))
	else:
		flash("You must be registered!", "warning")
		return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	'''Registration function checks if the user is already in session first and if true directs 
	to the classes page. If not, the function checks first if the password in two fields are identical. 
	If the test is not passed user is directed informed and the form is rendered again. 
	If the test is passes the rest of the form input will be validated for username, email 
	and password individually. 
	
	Username should be 6 to 30 char long and may consist unicode word characters and sign - only.

	Email is checked only for proper email formate, not if the mail is actually working 
	or the if domain is really existing.

	Password needs to have at least one lowercase, one uppercase, one special and one numeric character, 
	and have a length of 6 to 30 characters.

	Each validation can either pass to redirect the user to the classes page or return a warning message 
	and return the registration form.

	The code is modified from https://github.com/MiroslavSvec/DCD_lead/blob/master/app.py user authentication example.
	'''
	# Check if user is not logged in already
	if 'user' in session:
		flash('You are already signed in!', "success")
		return redirect(url_for('classes'))
	if request.method == 'POST':
		form = request.form.to_dict()
		# print(form)
		username = form['username']
		email = form['email']
		# If matched validate the username
		regex_in_name = '^[\w.-]+$'
		name_pattern = re.compile(regex_in_name)
		user = users_collection.find_one({"username" : username})
		if user:
			flash("Username " + username + " is already taken", "warning")
			# print('username taken')
			return render_template('register.html', username = username, email = email)
		elif len(username) < 6 or len(username) > 20:
			flash("Username must be at least 6 and up to 20 characters long", "warning")
			# print('wrong length')
			return render_template('register.html', username = username, email = email)
		elif not re.search(name_pattern, username):
			flash("Username may not have special characters", "warning")
			return render_template('register.html', username = username, email = email)
		else:
			# If username passes validate the email
			email = form['email']
			regex_in_mail = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
			email_pattern = re.compile(regex_in_mail)
			if not re.search(email_pattern, email):
				flash("Email is not valid!", "warning")
				return render_template('register.html', username = username, email = email)
			else:
				# If email passes validate password
				password = form['password']
				regex_in_password = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@$%#&*?])[A-Za-z\d!@$%#&*?]{6,20}$'
				password_pattern = re.compile(regex_in_password)
				if len(password) < 6 or len(password) > 20:
					flash("Password must be at least 6 and up to 20 characters long", "warning")
					# Search for regex in pw
					return render_template('register.html', username = username, email = email)
				elif not re.search(password_pattern, password):
					flash("Password is not valid!", "warning")
					return render_template('register', username = username, email = email)
				# Check if the passwords actually match
				elif form['password'] != form['password1']:
					# Notify user of not matching passwords
					flash("Passwords don't match! Try again.", "warning")
					return render_template('register.html', username = username, email = email)
				else:
					# Hash password
					hash_pass = generate_password_hash(form['password'])
					# Create new user with hashed password
					new_user = users_collection.insert_one({
						'username': form['username'],
						'email': form['email'],
						'password': hash_pass
						})
					user_Oid = new_user.inserted_id
					user_id = str(user_Oid)
					# Check if user is actually inserted
					user_in_db = users_collection.find_one({"username" : form['username']})
					if user_in_db:
						# Log user in (add to session)
						session['user'] = user_in_db['username']
						username = session['user']
						# Insert a new entry to the series collection for the user's class series.
						# The associate classes id will be added to the class_series array.
						series_collection.insert_one({
							'user_id': user_id,
							'username': username,
							'class_series': []
							})
						flash("You are registered, logged in and ready to go", "success")
						return redirect(url_for('classes', username = username))
						# If user was not inserted/added inform the user of error
					else:
						flash("There was a problem with registration, please try again", "warning")
						return render_template('register.html', username = username, email = email)
	return render_template('register.html', title="Register")


@app.route('/logout')
def logout():
	''' Function logs the user out by clearing the user from the session 
	and redirecting to the login page.
	'''
	# Clear the session
	session.clear()
	flash("Success! You were logged out", "success")
	return redirect(url_for('index'))


# Routes Handling CRUD operations for Classes

@app.route('/classes/<username>')
def classes(username):
	''' Function checks first if the user is added to the session. 
	If not the user is directed to the login page. If user is added to the session, 
	the function finds the user from the classes collection and renders the classes user
	has created on to the classes page to be viewed, edited, deleted or duplicated.
	'''
	# Check if user is logged in
	if 'user' in session:
		# If so get the user classes and pass them to a template
		# user_in_db = users_collection.find_one({'username': username})
		classes = classes_collection.find({'username': username})
		series = series_collection.find_one({'username': username})
		return render_template('classes.html', title = 'Classes',
								username = username, classes = classes, series = series,)
	else:
		flash("You must be logged in!", "warning")
		return redirect(url_for('index'))


# Handling CRUD operations for each Class in user's Classes
@app.route('/view_class/<class_id>')
def view_class(class_id):
	''' Function renders a selected class among the user's classes from the db classes collection.'''
	username = session['user']
	this_class = classes_collection.find_one({'_id' : ObjectId(class_id)})
	series = series_collection.find_one({'username' : session['user']})
	# This creates an array of class id's stored in 'series'.'class_series'.'classes' and stores it in var merged_list.
	# The list is used to check if THIS class is associated with any of the user's created series in series collection.
	merged_list = []
	for item in series['class_series']:
		for class_in_classes in item['classes']:
			merged_list.append(class_in_classes)
	return render_template('viewClass.html', title = 'Class', class_id = class_id, 
							this_class = this_class, username = username, series = series, merged_list = merged_list)


@app.route('/add_class/<username>')
def add_class(username):
	''' Function renders a add class form.

	In a form the user may choose to associate the class with a class series.
	Function finds the user's class series document from the db series collection.
	'''
	user = users_collection.find_one({'username': session['user']})
	series = series_collection.find_one({'username': session['user']},{'class_series': 1})
	return render_template('addClass.html', title="New Class", 
							user = user, username = username, series = series)


@app.route('/insert_class/<series_doc>/<username>', methods=['POST'])
def insert_class(series_doc, username):
	''' Function inserts a new class document to the db classes collection.

	If the user has selected a series to associate the class with, 
	the class id is stored in that series object class_series array, 
	located in the user's series document in db series collection.

	After the insert and confirmation the user is directed back to the class view. 
	After each iteration, the series update operation is checked and printed to the terminal.
	'''
	new_class = {
		'class_name': request.form.get('class_name'),
		'class_description': request.form.get('class_description'),
		'main_elements': request.form.get('editordata'),
		'other_elements': request.form.get('other_elements'),
		'playlist_title': request.form.get('playlist_title'),
		'playlist_link': request.form.get('playlist_link'),
		'class_notes': request.form.get('class_notes'),
		'exercises': [],
		'logs': [],
		'user_id': request.form.get('user_id'),
		'username': username
		}
	inserted_class = classes_collection.insert_one(new_class)
	this_class = inserted_class
	class_Oid = inserted_class.inserted_id
	class_id = str(class_Oid)
	series_in_form = request.form.getlist('series')
		# Loop through each of the series collection class_series Array of series objects.
		# In each object, loop through the classes Arrays and find which class_series ObjectId equals to the id passed from the selected series option value
	for item in series_in_form:
		# Push the class_id to the Array
		series_collection.update_one(
			{'_id': ObjectId(series_doc), 'class_series._id': ObjectId(item)}, 
			{ '$push': { 'class_series.$.classes': class_id }}
			)
		#Check if the class_id was pushed to the array
		array = series_collection.find_one(
			{ '_id': ObjectId(series_doc) }, 
			{ 'class_series': {'$elemMatch': { '_id': ObjectId(item)}}}
			)
		if not array:
			print('Class was not added to ' + item)
		else:
			print('Class was added to ' + item + 'successfully')
	return redirect(url_for('view_class', class_id=class_id, 
					username=username, this_class=this_class))

@app.route('/edit_class/<class_id>')
def edit_class(class_id):
	''' Function renders an edit class view with an edit form.
	Function finds the user's series document for the select series 
	function on the edit class page.
	'''
	user = users_collection.find_one({'username': session['user']})
	this_class =  classes_collection.find_one({"_id": ObjectId(class_id)})
	class_id = class_id
	series = series_collection.find_one({'username': session['user']})
	return render_template('editClass.html', title="Edit Class", user = user, 
							class_id = class_id, this_class = this_class, series = series)


@app.route('/save_class/<class_id>/<series_doc>', methods=['GET','POST'])
def save_class(class_id, series_doc):
	''' Function updates the class after edit.

	The series document is also updated. First the removes the class id reference 
	from all series objects class_series Arrays. Then the class id reference is 
	added to the selected series class_series Arrays and finally the series update 
	operation is checked and printed to the terminal after each iteration.

	The user is directed to the view class page.
	'''
	updated_class = classes_collection.update_one(
		{'_id': ObjectId(class_id)},
		{ '$set': { 'class_name': request.form.get('class_name'),
		'class_description': request.form.get('class_description'),
		'main_elements': request.form.get('editordata'),
		'other_elements': request.form.get('other_elements'),
		'playlist_title': request.form.get('playlist_title'),
		'playlist_link': request.form.get('playlist_link'),
		'class_notes': request.form.get('class_notes'),
		'user_id': request.form.get('user_id'),
		'username': request.form.get('username')}}
		)
	series_in_form = request.form.getlist('series')
	# Remove the class id from each of the series collection class_series array of objects classes arrays
	series_collection.update_many(
		{'_id': ObjectId(series_doc)}, 
		{'$pull': {'class_series.$[].classes': class_id}}, 
		upsert = False
		)
	# Loop through each of the series collection class_series array of objects classes arrays where the class_series ObjectId equals to id passed from the selected series option value
	for item in series_in_form:
		# Push the class_id to the Array
		series_collection.update_one(
			{'_id': ObjectId(series_doc), 'class_series._id': ObjectId(item)}, 
			{ '$push': { 'class_series.$.classes': class_id} }
			)
		# Check if the class_id was pushed to the array
		array = series_collection.find_one({ '_id': ObjectId(series_doc) }, 
			{ 'class_series': {'$elemMatch': { '_id': ObjectId(item)}}}
			)
		if not array:
			print('Class was not added to ' + item)
		else:
			print('Class was added to ' + item + 'succesfully')
	return redirect(url_for('view_class', class_id = class_id ))


@app.route('/delete_class/<class_id>/<series_doc>/<username>')
def delete_class(class_id, series_doc, username):
	''' Function deletes the selected class document from the db classes collection, 
	and returns user to the classes view.
	'''
	deleted_class = classes_collection.remove({'_id': ObjectId(class_id)})
		# From each series document series object in sereis Array, remove the deleted class id.
	series_collection.update_many({'_id': ObjectId(series_doc)}, 
		{'$pull': {'class_series.$[].classes': class_id}}, 
		upsert = False
		)
	flash("Class was removed!", "danger")
	return redirect(url_for('classes', username = username))


@app.route('/copy_class/<class_id>')
def copy_class(class_id):
	''' Function duplicates a class document, by inserting it in to the classes collection 
	without id. Original id field is first removed. MongoDB will add a new ObjectId automaticall 
	to the document when it is inserted.A (copy) prefix is added to the class to clarify the class 
	in question is a duplicate. The Logs belonging to the original class document are also removed.

	User is directed to the edit class view of the duplicate class.
	'''
	copy_this  = classes_collection.find_one({'_id': ObjectId(class_id)})
	# Create a postfix (copy) for the class_name
	name = copy_this['class_name']
	postfix = '(copy)'
	edit_name = ''.join((name, postfix))
	# Remove _id field from copy_this class document
	del copy_this['_id']
	duplicated = classes_collection.insert_one(copy_this)
	duplicate = duplicated.inserted_id
	remove_name_and_logs = classes_collection.update_one({'_id': ObjectId(duplicate)}, 
		{ '$set': { 'class_name': edit_name, 'logs': [] }}
		)
	flash("Success! Class was duplicated", 'success')
	return redirect(url_for('edit_class', title="Edit Class(copy)", class_id = duplicate))


# Handling CRUD operations of Logs in Class
@app.route('/add_log/<class_id>/<username>')
def add_log(class_id, username):
	''' Function renders an add log page.'''
	return render_template('addLog.html', title="Add Log", 
							class_id = class_id, username = username)


@app.route('/insert_log/<class_id>', methods=['POST'])
def insert_log(class_id):
	''' Function finds a class and adds a new log object to the logs 
	Array embedded into the class document in db classes collection.

	User is directed back to the class view.
	'''
	new_log = {
		'_id': ObjectId(),
		'log_date': request.form.get('log_date'),
		'log_text': request.form.get('editordata'),
		'log_tag': request.form.get('log_tag')
	}
	inserted_log = classes_collection.update_one({'_id': ObjectId(class_id)}, 
		{ '$addToSet' :{ 'logs': new_log}}
		)
	return redirect(url_for('view_class', class_id = class_id))


@app.route('/edit_log/<class_id>/<log_id>', methods=['GET', 'POST'])
def edit_log(class_id, log_id):
	''' Function renders an edit log view.'''
	this_log = classes_collection.find_one({'_id': ObjectId(class_id)}, 
	{'logs': {"$elemMatch": {'_id': ObjectId(log_id)}}}
	)
	log = this_log['logs']
	return render_template('editLog.html', title='Edit log', 
							log = log, class_id = class_id, log_id = log_id)


@app.route('/update_log/<class_id>/<log_id>', methods=['POST'])
def update_log(class_id, log_id):
	''' Function finds and updates the edited log entry in class document 
	in db classes collection.

	User is directed back to the class view.
	'''
	update_log = classes_collection.update_one(
		{'_id': ObjectId(class_id), 'logs._id': ObjectId(log_id)}, 
		{'$set': {'logs.$.log_date': request.form.get('log_date'),
		'logs.$.log_text': request.form.get('editordata'),
		'logs.$.log_tag': request.form.get('log_tag')}}
		)
	return redirect(url_for('view_class', class_id = class_id))

@app.route('/delete_log/<class_id>/<log_id>')
def delete_log(class_id, log_id):
	'''
	Function finds and deletes the selected log entry form the class document 
	in db classes collection.

	User is directed back to the class view.
	'''
	deleted_log = classes_collection.update_one(
		{'_id': ObjectId(class_id)}, 
		{'$pull': { 'logs': {'_id': ObjectId(log_id)}}}
		)
	flash("Log was removed!", "danger")
	return redirect(url_for('view_class', class_id = class_id))


# Handling CRUD operations for Exercises in Class
@app.route('/add_exercise/<class_id>')
def add_exercise(class_id):
	'''
	Function renders an add exercise page.
	'''
	return render_template('addExercise.html', title='New exercise', class_id=class_id)


@app.route('/insert_exercise/<class_id>', methods=['POST'])
def insert_exercise(class_id):
	''' Function finds a class and adds a new exercise object to the exercises 
	Array embedded into the class document in db classes collection.

	User is directed back to the class view.
	'''
	new_exercise = {
		'_id': ObjectId(),
		'exercise_name': request.form.get('exercise_name'),
		'exercise_description': request.form.get('editordata'),
		'exercise_comment': request.form.get('exercise_comment'),
		'exercise_aim': request.form.get('exercise_aim'),
		'tracks': [],
		'links': []
	}
	inserted_exercise = classes_collection.update_one(
		{'_id': ObjectId(class_id)}, 
		{ '$addToSet': { 'exercises': new_exercise}}
		)
	return redirect(url_for('view_class', class_id=class_id))


@app.route('/edit_exercise/<class_id>/<exercise_id>', methods=['GET','POST'])
def edit_exercise(class_id, exercise_id):
	''' Function renders an edit exercise view with an edit form. '''
	this_exercise = classes_collection.find_one(
		{'_id': ObjectId(class_id)}, 
		{'exercises': {"$elemMatch": {'_id': ObjectId(exercise_id)}}}
		)
	return render_template('editExercise.html', title='Edit exercise', 
							this_exercise = this_exercise, class_id = class_id, 
							exercise_id = exercise_id)

@app.route('/update_exercise/<class_id>/<exercise_id>', methods=['POST'])
def update_exercise(class_id, exercise_id):
	''' Function finds and updates the edited exercise entry in class document 
	in db classes collection.

	User is directed back to the class view.
	
	To tackle the issue of updating a sub-documents in obejct arrays:
	https://stackoverflow.com/questions/36841911/mongodb-update-complex-document?noredirect=1&lq=1
	provided the information I needed to formulate the correct syntax
	'''
	updated_exercise = classes_collection.update_one(
		{'_id': ObjectId(class_id), 'exercises._id': ObjectId(exercise_id)}, 
		{'$set': {'exercises.$.exercise_name': request.form.get('exercise_name'),
		'exercises.$.exercise_description': request.form.get('editordata'),
		'exercises.$.exercise_comment': request.form.get('exercise_comment'),
		'exercises.$.exercise_aim': request.form.get('exercise_aim')}}
		)
	return redirect(url_for('view_class', class_id=class_id))

@app.route('/delete_exercise/<class_id>/<exercise_id>')
def delete_exercise(class_id, exercise_id):
	''' Function finds and deletes the selected exercise entry form the class document 
	in db classes collection.

	User is directed back to the class view.
	'''
	deleted_exercise = classes_collection.update_one(
		{'_id': ObjectId(class_id)}, 
		{'$pull': { 'exercises': {'_id': ObjectId(exercise_id)}}}
		)
	flash("Exercise was removed!", "danger")
	return redirect(url_for('view_class', class_id=class_id))


#  Handling CRUD operations of Music Tracks in Exercises in Class
@app.route('/add_track/<class_id>/<exercise_id>')
def add_track(class_id, exercise_id):
	''' Function renders an add music track view. '''
	return render_template('addTrack.html', title="Music Track", 
							class_id = class_id, exercise_id = exercise_id)


@app.route('/insert_track/<class_id>/<exercise_id>', methods=['POST'])
def insert_track(class_id, exercise_id):
	''' Function finds the exercise object embedded in the class document 
	in db classes collection.

	A new music track object is inserted to the exercise tracks Array.

	User is directed back to the class view. 
	'''
	new_track = {
		'_id': ObjectId(),
		'track_title': request.form.get('track_title'),
		'track_link': request.form.get('track_link'),
		'track_comment': request.form.get('track_comment')
	}
	inserted_track = classes_collection.update_one(
		{'_id': ObjectId(class_id), 'exercises._id':ObjectId(exercise_id)}, 
		{ '$addToSet': {'exercises.$.tracks' : new_track}}
		)
	return redirect(url_for('view_class', class_id = class_id))


@app.route('/delete_track/<class_id>/<exercise_id>/<track_id>')
def delete_track(class_id, exercise_id, track_id):
	''' Function finds and deletes the selected music track object form the class document 
	in db classes collection.

	User is directed back to the class view.
	'''
	deleted_track = classes_collection.update_one(
		{'_id': ObjectId(class_id), 'exercises._id':ObjectId(exercise_id)}, 
		{'$pull': { 'exercises.$.tracks': { '_id': ObjectId(track_id)}}}
		)
	return redirect(url_for('view_class', class_id = class_id))


# Handling CRUD operations of Video Links in exercises in Classes

@app.route('/add_link/<class_id>/<exercise_id>')
def add_link(class_id, exercise_id):
	''' Function renders an add video link view. '''
	return render_template('addLink.html', title="Video link", 
							class_id = class_id, exercise_id = exercise_id)

@app.route('/insert_link/<class_id>/<exercise_id>', methods=['POST'])
def insert_link(class_id, exercise_id):
	''' Function finds the exercise object embedded in the class document 
	in db classes collection.

	A new video link object is inserted to the exercise tracks Array.

	User is directed back to the class view. 
	'''
	new_link = {
		'_id': ObjectId(),
		'video_title': request.form.get('video_title'),
		'video_link': request.form.get('video_link'),
		'video_comment': request.form.get('video_comment')
	}
	inserted_link = classes_collection.update_one(
		{'_id': ObjectId(class_id), 'exercises._id':ObjectId(exercise_id)}, 
		{ '$addToSet': {'exercises.$.links' : new_link}}
		)
	return redirect(url_for('view_class', class_id = class_id))


@app.route('/delete_link/<class_id>/<exercise_id>/<link_id>')
def delete_link(class_id, exercise_id, link_id):
	''' Function finds and deletes the selected video link object form the class document 
	in db classes collection.

	User is directed back to the class view.
	'''
	deleted_link = classes_collection.update_one(
		{'_id': ObjectId(class_id), 'exercises._id':ObjectId(exercise_id)}, 
		{'$pull': { 'exercises.$.links': { '_id': ObjectId(link_id)}}}
		)
	return redirect(url_for('view_class', class_id = class_id))


# Handling CRUD operatins of Class Series
@app.route('/series')
def series():
	''' Function checks first if the user is added to the session. 
	If not the user is directed to the login page. If user is added to the session, 
	the function finds the user from the db series collection and renders the series user
	has created on to the series page to be viewed, edited or deleted.
	'''
	# Check if user is logged in
	if 'user' in session:
		# If so get the user classes and pass them to a template
		user_in_db = users_collection.find_one({'username': session['user']})
		username = session['user']
		all_series = series_collection.find_one({'username': username})
		return render_template('series.html',
						title = 'Series',
						username = username,
						all_series = all_series,
						user_in_db = user_in_db)
	else:
		flash("You must be logged in!", "warning")
		return redirect(url_for('index'))


@app.route('/view_classes_in_series/<username>/<series_id>/<series_doc>')
def view_classes_in_series(username, series_id, series_doc):
	''' Function finds the user from the db series collection and renders the classes 
	associated with the selected series on to the view classes in series page 
	to be viewed, edited, deleted or duplicated.
	'''
	series = series_collection.find_one({'username': username})
	# Find specific serial (with _id: series_id) in series document (with _id: series_doc)
	serial = series_collection.find_one(
		{ '_id' : ObjectId(series_doc) }, 
		{ 'class_series' : {'$elemMatch' : { '_id': ObjectId(series_id)}}}
		)
	serial_name = serial
	# Find all classes of the user
	all_classes = classes_collection.find({'username': username})
	return render_template('view_classes_in_series.html', title="Classes in Series", serial = serial,
							serial_name = serial_name, all_classes = all_classes, username = username, series = series)


@app.route('/add_series')
def add_series():
	''' Function renders an add series view. 
	
	Also, in case the user has no series document yet created into the db series collection,
	it is added
	'''
	username = session['user']
	user_id = users_collection.find_one({'username': session['user']}, {'_id': 1})
	# This checks if the user already has a document in series collection, if not a document will be added.
	# https://stackoverflow.com/questions/25163658/mongodb-return-true-if-document-exists 
	# answer by Xavier Guihot led to the right path with this.
	if series_collection.count_documents({'username': session['user']}, limit = 1) == 0:
		new_user_document = {
			'user_id': user_id._id,
			'username': username,
			'class_series': []
			}

		inserted_document = series_collection.insert_one(new_user_document)
		series_id = inserted_document.inserted_id
	return render_template('addSeries.html', title="Add Series", 
							user_id = user_id, username = username)


@app.route('/insert_series/<username>', methods=['GET', 'POST'])
def insert_series(username):
	''' Function adds a new series object into the series document series Array 
	in db series collection.

	User is directed back to the series view.
	'''
	new_series_item = {
		'_id': ObjectId(),
		'series_name': request.form.get('series_name'),
		'series_description': request.form.get('series_description'),
		'classes': []
		}
	inserted_item = series_collection.update_one({'username': username},
												 { '$addToSet' : { 'class_series': new_series_item}})
	return redirect(url_for('series', title='Series', username=username ))


@app.route('/edit_series/<series_doc>/<series_id>', methods=['GET', 'POST'])
def edit_series(series_doc, series_id):
	''' Function finds the selected series object from the series document series Array and 
	renders an edit series view. 
	'''
	this_series = series_collection.find_one(
		{'_id': ObjectId(series_doc)}, 
		{ 'class_series' : {'$elemMatch': { '_id': ObjectId(series_id)}}}
		)
	return render_template('editSeries.html', title='Edit series', 
							this_series = this_series, series_doc=series_doc, series_id = series_id)


@app.route('/update_series/<series_doc>/<series_id>', methods=['GET', 'POST'])
def update_series(series_doc, series_id):
	''' Function finds and updates the series object in the series document series Array.'''
	updated_series = series_collection.update_one(
		{'_id': ObjectId(series_doc), 'class_series._id': ObjectId(series_id)}, 
		{'$set' : {'class_series.$.series_name' : request.form.get('series_name'),
		'class_series.$.series_description': request.form.get('series_description')}}
		)
	return redirect(url_for('series'))


@app.route('/delete_series/<series_id>/<series_doc>', methods=["GET"])
def delete_series(series_doc, series_id):
	''' Function deletes the selected series object from the series document series Array.'''
	deleted_series = series_collection.update_one(
		{'_id': ObjectId(series_doc)}, 
		{ '$pull' : { 'class_series' : {'_id': ObjectId(series_id)}}}
		)
	flash("Series was removed!", "danger")
	return redirect(url_for('series', series_id = series_id))


if __name__ == '__main__':

	app.run(host = os.environ.get('IP'),
		port = int(os.environ.get('PORT')),
		debug = True)
 