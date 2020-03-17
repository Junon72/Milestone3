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
			return redirect(url_for('classes', username = user_in_db['username']))
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



###################################### Handling Classes / CRUD #################################

# VIEW CLASSES
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

# VIEW CLASS
@app.route('/view_class/<class_id>')
def view_class(class_id):
    username = session['user']
    this_class = classes_collection.find_one({'_id': ObjectId(class_id)})
    class_id = class_id
    series = classes_collection.find_one({'_id': ObjectId(class_id)}, {'series': 1})
    print(this_class)
    print(class_id)
    print(series)
    return render_template('viewClass.html', 
                               title = 'Class',
                               class_id = class_id,  
                               this_class = this_class,
                               username = username,
                               series = series)

# ADD CLASS
@app.route('/add_class')
def add_class():
    user = users_collection.find_one({'username': session['user']})
    print(user)
    series = series_collection.find_one({'username': session['user']},{'class_series': 1})
    print(series)
    return render_template('addClass.html', title="New Class", 
                           user = user, series = series)

# insert() CLASS FROM save COMES HERE
@app.route('/insert_class', methods=['POST'])
def insert_class():
    username = session['user']
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
    classes_collection.update_many(
        {'_id': ObjectId(class_id)},
        { '$set': { 'series': series}})
    return redirect(url_for('view_class', class_id=class_id, username=username, this_class=this_class ))

# EDIT CLASS
@app.route('/edit_class/<class_id>')
def edit_class(class_id):
    user = users_collection.find_one({'username': session['user']})
    this_class =  classes_collection.find_one({"_id": ObjectId(class_id)})
    print(this_class)
    class_id = class_id
    print(class_id)
    series = series_collection.find_one({'username': session['user']})
    print(series)
    return render_template('editClass.html', title="Edit Class", user = user, class_id = class_id, this_class = this_class, series = series)


# save() CLASS COMES HERE -> 
@app.route('/save_class/<class_id>', methods=['GET','POST'])
def save_class(class_id):
    
    updated_class = classes_collection.update(
        {'_id': ObjectId(class_id)},
        { '$set':
        { 'class_name': request.form.get('class_name'),
        'class_description': request.form.get('class_description'),
        'main_elements': request.form.get('main_elements'),
        'other_elements': request.form.get('other_elements'),
        'playlist_title': request.form.get('playlist_title'),
        'playlist_link': request.form.get('playlist_link'),
        'series': [],
        'class_notes': request.form.get('class_notes'),
        'user_id': request.form.get('user_id'),
        'username': request.form.get('username')}})
    print(updated_class)
    series = request.form.getlist('series')
    print(series)
    classes_collection.update_many(
        {'_id': ObjectId(class_id)},
        { '$set': { 'series': series}})
    return redirect(url_for('view_class', class_id = class_id ))

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
@app.route('/add_log/<class_id>/<username>')
def add_log(class_id, username):
    print(class_id)
    return render_template('addLog.html', class_id = class_id, username = username)
                 
# insert log - $addToSet{}
@app.route('/insert_log/<class_id>', methods=['POST'])
def insert_log(class_id):
    new_log = {
        '_id': ObjectId(),
        'log_date': request.form.get('log_date'),
        'log_text': request.form.get('log_text'),
        'log_tag': request.form.get('log_tag')  
	}
    inserted_log = classes_collection.update_one({'_id': ObjectId(class_id)}, { '$addToSet' :{ 'logs': new_log}})
    print(inserted_log)
    return redirect(url_for('view_class', class_id = class_id))

# EDIT LOG
@app.route('/edit_log/<class_id>/<log_id>', methods=['GET', 'POST'])
def edit_log(class_id, log_id):
    print(log_id)
    this_log = classes_collection.find_one({'_id': ObjectId(class_id)}, {'logs': {"$elemMatch" : {'_id': ObjectId(log_id)}}})
    print(this_log)
    return render_template('editLog.html', title='Edit log', this_log = this_log, class_id = class_id, log_id = log_id)

# UPDATE LOG
@app.route('/update_log/<class_id>/<log_id>', methods=['POST'])           
def update_log(class_id, log_id):
    update_log = classes_collection.update_one({'_id': ObjectId(class_id), 'logs._id': ObjectId(log_id)}, {'$set': {
        'logs.$.log_date': request.form.get('log_date'),
        'logs.$.log_text': request.form.get('log_text'),
        'logs.$.log_tag': request.form.get('log_tag')
    }})
    print(update_log)
    return redirect(url_for('view_class', class_id = class_id))

# DELETE LOG - $pull{}
@app.route('/delete_log/<class_id>/<log_id>')           
def delete_log(class_id, log_id):
    deleted_log = classes_collection.update_one({'_id': ObjectId(class_id)}, {'$pull': { 'logs': {'_id': ObjectId(log_id)}}} )
    print(deleted_log)
    return redirect(url_for('view_class', class_id = class_id))


###################################### Handling Exercises / CRUD #################################

# ADD EXERCISE
@app.route('/add_exercise/<class_id>')
def add_exercise(class_id):
    return render_template('addExercise.html', title='New exercise', class_id=class_id)

# insert exercise - $addToSet()
@app.route('/insert_exercise/<class_id>', methods=['POST'])
def insert_exercise(class_id):
    new_exercise = {
        '_id': ObjectId(),
        'exercise_name': request.form.get('exercise_name'),
        'exercise_description': request.form.get('exercise_description'),
        'exercise_comment': request.form.get('exercise_comment'),
        'exercise_aim': request.form.get('exercise_aim'),
        'tracks': [],
        'links': []
    }
    inserted_exercise = classes_collection.update_one({'_id': ObjectId(class_id)}, { '$addToSet' :{ 'exercises': new_exercise}})
    print(inserted_exercise)
    return redirect(url_for('view_class', class_id=class_id))

# EDIT EXERCISE
@app.route('/edit_exercise/<class_id>/<exercise_id>', methods=['GET','POST'])
def edit_exercise(class_id, exercise_id):
    print(exercise_id)
    this_exercise = classes_collection.find_one({'_id': ObjectId(class_id)}, {'exercises': {"$elemMatch" : {'_id': ObjectId(exercise_id)}}})
    print(this_exercise)
    return render_template('editExercise.html', title='Edit exercise', this_exercise = this_exercise, class_id = class_id, exercise_id = exercise_id)

# update() EXERCISE COMES HERE
@app.route('/update_exercise/<class_id>/<exercise_id>', methods=['POST'])
def update_exercise(class_id, exercise_id):
    print(exercise_id)
    updated_exercise = classes_collection.update_one(
        {'_id': ObjectId(class_id), 'exercises._id': ObjectId(exercise_id)}, {'$set': {
        'exercises.$.exercise_name': request.form.get('exercise_name'),
        'exercises.$.exercise_description': request.form.get('exercise_description'),
        'exercises.$.exercise_comment': request.form.get('exercise_comment'),
        'exercises.$.exercise_aim': request.form.get('exercise_aim')}})
    print(updated_exercise)
    return redirect(url_for('view_class', class_id=class_id))

# DELETE EXERCISE
@app.route('/delete_exercise')
def delete_exercise():
    deleted_exercise = classes_collection.update_one({'_id': ObjectId(class_id)}, {'$pull': { 'exercises': {'_id': ObjectId(exercise_id)}}} )
    print("Exercise was deleted")
    return redirect(url_for('view_class'))


######################################  Handling Music Tracks / CRUD 

 # ADD MUSIC TRACK
@app.route('/add_track/<class_id>/<exercise_id>', methods=['POST'])
def add_track(class_id, exercise_id):
    print(class_id)
    print(exercise_id)
    return render_template('addTrack.html', title="Music Track", class_id = class_id, exercise_id = exercise_id)

# insert() track
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
    deleted_track = classes_collection.update({'_id': ObjectId(class_id)}, { 'exercises' : {'$pull': { 'tracks': { 'tracks_id': ObjectId(track_id)}}}})
    return redirect(url_for('view_class'))


##################################### Handling Video Links / CRUD 

# ADD VIDEO LINK
@app.route('/add_link/<class_id>/<exercise_id>', methods=['POST'])
def add_link(class_id, exercise_id):
    print("Link was added")
    return render_template('addLink.html', title="Video link", )

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


###################################### Handling Class Series / CRUD #################################

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
        new_user_document = {
            'user_id': user_id,
            'username': username,
            'class_series': []
            }
        
        inserted_document = series_collection.insert_one(new_user_document)
        series_id = inserted_document.inserted_id
        print(doc)
    return render_template('addSeries.html', title="Add Series", user_id = user_id, username = username)

# insert series - $addToSet
@app.route('/insert_series/<username>', methods=['GET', 'POST'])
def insert_series(username):
    new_series_item = {
        '_id': ObjectId(),
        'series_name': request.form.get('series_name'),
        'series_description': request.form.get('series_description'),
        'classes': []
        }
    inserted_item = series_collection.update_one({'username': username}, { '$addToSet' :{ 'class_series': new_series_item}})
    print(inserted_item)
    return redirect(url_for('series', title='Series', username=username ))
    
# EDIT SERIES
@app.route('/edit_series/<series_doc>/<series_id>')
def edit_series(series_doc, series_id):
    username = session['user']
    print(series_doc)
    return render_template('editSeries.html', title='Edit series', series_doc=series_doc, series_id = series_id)

# update() SERIES COMES HERE
@app.route('/update_series/<series_id>', methods=['POST'])
def update_series(series_id):
    print(series_doc, series_id)
    return redirect(url_for('series'))

# DELETE CLASS SERIES - remove()
@app.route('/delete_series/<series_id>')
def delete_series(series_doc, series_id):
    deleted_series = series_collection.update_one({'_id': ObjectId(series_doc)}, { '$pull' : { 'class_series' : {'_id': ObjectId(series_id)}}} )
    print(deleted_series)
    return redirect(url_for('series'))


if __name__ == '__main__': 

   app.run(host=os.environ.get('IP'),             
                                                  
      port=int(os.environ.get('PORT', 5000)),
      debug=True)           