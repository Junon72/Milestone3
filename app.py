import os
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, url_for, session, flash
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
		# Check if the password and password1 actually match 
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
                               classes = classes_collection.find({'username': session['user']}))
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

# insert() CLASS COMES HERE
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
                 'series': request.form.to_dict({'name'}),
                 'class_notes': request.form.get('class_notes'),
                 'exercises': [{}],
                 'logs': [{}],
                 'user_id': request.form.get('user_id'),
                 'username': request.form.get('username')}
    
    print(new_class)
    inserted_class = classes_collection.insert_one(new_class)
    print(inserted_class)
    this_class = inserted_class
    class_id = inserted_class.inserted_id
    print(class_id)
    return redirect(url_for('view_class', class_id=class_id, username=username, this_class=this_class ))

# EDIT CLASS
@app.route('/edit_class/<class_id>')
def edit_class(class_id):
    username = session['user']
    user_id = users_collection.find_one({'username': session['user']})
    print(user_id)
    this_class =  classes_collection.find({"_id": ObjectId(class_id)})
    print(this_class)
    class_id = class_id
    print(class_id)
    series = series_collection.find({'username': username})
    print(series)
    return render_template('editClass.html', title="Edit Class", this_class = this_class, class_id = class_id)


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
@app.route('/add_log')
def add_log():
    print('Log was added')
    return render_template('addLog.html')
                 
# save() log
@app.route('/insert_log', methods=['POST'])
def insert_log():
    print('Log was inserted')
    return redirect(url_for('editClass', title='Edit Class'))

# DELETE LOG - remove()
@app.route('/delete_log')           
def delete_log():
    print('Log was deleted')
    return redirect(url_for('editClass', title='Edit Class')

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
    # return redirect(url_for('edit_class'))

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
@app.route('/add_track', methods=['POST'])
def add_track():
    print("Track was added")
    return render_template(url_for('addTrack'), title="Music Track")

# insert() track
@app.route('/insert_track', methods=['POST'])
def insert_track():
    print("Track was inserted")
    return redirect(url_for('edit_exercise'), title='Edit Exercise')

# DELETE MUSIC  TRACK- remove() 
@app.route('/delete_track')
def delete_track():
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
    print("Series view opened")            
    return render_template(url_for('series'), title='Series')

# VIEW CLASSES IN SERIES
@app.route('/view_classes_in_series', methods=['GET'])           
def view_classes_in_series(): 
    print("Classes in series view opened")            
    return render_template(url_for('classes'), title='Classes in series')

# ADD CLASS SERIES
@app.route('/add_series', methods=['POST'])
def add_series():
    print("Series was added")
    return render_template(url_for('addSeries'), title="Add Series")

# insert() series
@app.route('/insert_series', methods=['POST'])
def insert_series():
    print("Series was inserted")
    return redirect(url_for('series', title='Series'))

# EDIT SERIES
@app.route('/edit_series', methods=['GET'])
def edit_series():
    print('Exercise was edited')
    return render_template(url_for('editSeries'), title='Edit series')

# update() SERIES COMES HERE
@app.route('/update_series', methods=['POST'])
def update_series():
    print("Series was updated")
    return redirect(url_for('series'), title='Series')

# DELETE CLASS SERIES - remove()
@app.route('/delete_series', methods=['GET'])
def delete_series():
    print("Series was deleted")
    return redirect(url_for('series'), title='Series')


if __name__ == '__main__': 

   app.run(host=os.environ.get('IP'),             
                                                  
      port=int(os.environ.get('PORT', 5000)),
      debug=True)           