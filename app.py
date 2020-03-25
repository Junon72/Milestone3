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
from ast import literal_eval



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

# url vars
# back to classes view
back_to_classes = {
    "button_text": "Back to Classes",
    "url_name" : "classes"
}
# back to classes in series view
back_to_series = [{
    "button_text": "Back to Classes",
    "url_name" : "view_classes_in_series"
}]

@app.route('/')

###################################### LOGIN/OUT AND REGISTERING #################################

# LOGIN - html/ form
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

# CHECK USER LOGIN DETAILS FROM LOGIN FORM AND COMPARE WITH THE USER DATA IN USERS COLLECTION
@app.route('/user_auth', methods=['POST'])
def user_auth():
	form = request.form.to_dict()
	user_in_db = users_collection.find_one({'username': form['username']})
	# Check for user in database
	if user_in_db:
		# If passwords match (hashed / real password)
		if check_password_hash(user_in_db['password'], form['password']):
			# Log user in (add to session)
			session['user'] = form['username']
			return redirect(url_for('classes', username=user_in_db['username']))
			
		else:
			flash("Wrong password or user name!")
			return redirect(url_for('index'))
	else:
		flash("You must be registered!")
		return redirect(url_for('register'))

# SIGN UP A NEW USER - html/ form - insert_one()
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
			# If user does not exist register new user - insert user to user collection
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
				# Check if user is actually inserted
				user_in_db = users_collection.find_one({"username": form['username']})
				if user_in_db:
					# Log user in (add to session)
					session['user'] = user_in_db['username']
					return redirect(url_for('/index', user=user_in_db['username']))
                    # If user was not inserted/added inform the user of error
				else:
					flash("There was a problem with registration, please try again")
					return redirect(url_for('register'))

		else:
            # Notify user of not matching passwords
			flash("Passwords don't match! Try again.")
			return redirect(url_for('register'))
		
	return render_template('register.html')

# LOGOUT USER AND RETURN TO LOGIN PAGE
@app.route('/logout')
def logout():
	# Clear the session
	session.clear()
	flash('You were logged out!')
	return redirect(url_for('index'))


###################################### Handling Classes / CRUD #################################

# VIEW ALL CLASSES IN USER'S COLLECTION - html/ view
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
        series = series_collection.find_one({'username': username})
        return render_template('classes.html',
                               title = 'Classes', 
                               username = username, 
                               classes = classes,
                               series = series,
                               back_to_classes = back_to_classes)
    else:
    	flash("You must be logged in!")
    	return redirect(url_for('index'))
 
###################################### Handling Class in Classes / CRUD #################################

# VIEW CLASS IN COLLECTION - html/ view
@app.route('/view_class/<class_id>')
def view_class(class_id):
    username = session['user']
    this_class = classes_collection.find_one({'_id': ObjectId(class_id)})
    class_id = class_id
    series = series_collection.find_one({'username': session['user']})
    # print('this_class', this_class)
    # print('class_id', class_id)
    # print('series', series)
    # print(type(go_back_passed))
    '''
    go_back = {
        'button_text': request.form.get('button_text'),
        'url_name': request.form.get('url_name')
    }
   
    print('go back', go_back)
     '''
    return render_template('viewClass.html', 
                               title = 'Class',
                               class_id = class_id,  
                               this_class = this_class,
                               username = username,
                               series = series,
                               go_back = back_to_classes)

# ADD CLASS - html/ form
@app.route('/add_class')
def add_class():
    user = users_collection.find_one({'username': session['user']})
    # print(user)
    series = series_collection.find_one({'username': session['user']},{'class_series': 1})
    # rint(series)
    return render_template('addClass.html', title="New Class", 
                           user = user, series = series)

# INSERT NEW CLASS TO COLLECTION - insert_one()
@app.route('/insert_class/<series_doc>', methods=['POST'])
def insert_class(series_doc):
    username = session['user']
    new_class = {'class_name': request.form.get('class_name'),
                 'class_description': request.form.get('class_description'),
                 'main_elements': request.form.get('main_elements'),
                 'other_elements': request.form.get('other_elements'),
                 'playlist_title': request.form.get('playlist_title'),
                 'playlist_link': request.form.get('playlist_link'),
                 'class_notes': request.form.get('class_notes'),
                 'exercises': [],
                 'logs': [],
                 'user_id': request.form.get('user_id'),
                 'username': request.form.get('username')}
    # print(new_class)
    inserted_class = classes_collection.insert_one(new_class)
    # print(inserted_class)
    this_class = inserted_class
    class_Oid = inserted_class.inserted_id
    class_id = str(class_Oid)
    # print('new class id', class_id)
    series_in_form = request.form.getlist('series')
    # print('series in', series_in_form)
        #Loop through each of the series collection class_series array of objects classes arrays where the class_series ObjectId equals to id passed from the selected series option value
    for item in series_in_form:
        # Push the class_id to the Array
        series_collection.update_one({'_id': ObjectId(series_doc), 'class_series._id': ObjectId(item)}, { '$push': { 'class_series.$.classes': class_id } })
        #Check if the class_id was pushed to the array
        array = series_collection.find_one({ '_id': ObjectId(series_doc) }, { 'class_series': {'$elemMatch': { '_id': ObjectId(item)}}})
        # print(array)

    return redirect(url_for('view_class', class_id=class_id, username=username, this_class=this_class ))

# EDIT CLASS - html/ form
@app.route('/edit_class/<class_id>')
def edit_class(class_id):
    user = users_collection.find_one({'username': session['user']})
    this_class =  classes_collection.find_one({"_id": ObjectId(class_id)})
    # print('this class', this_class)
    # print(type(this_class))
    class_id = class_id
    # print(class_id)
    series = series_collection.find_one({'username': session['user']})
    # print('series in collection', series)
    return render_template('editClass.html', title="Edit Class", user = user, class_id = class_id, this_class = this_class, series = series)


# UPDATE CLASS AFTER EDIT - update_one()
@app.route('/save_class/<class_id>/<series_doc>', methods=['GET','POST'])
def save_class(class_id, series_doc):
    updated_class = classes_collection.update_one(
        {'_id': ObjectId(class_id)},
        { '$set':
        { 'class_name': request.form.get('class_name'),
        'class_description': request.form.get('class_description'),
        'main_elements': request.form.get('main_elements'),     
        'other_elements': request.form.get('other_elements'),
        'playlist_title': request.form.get('playlist_title'),
        'playlist_link': request.form.get('playlist_link'),
        'class_notes': request.form.get('class_notes'),
        'user_id': request.form.get('user_id'),
        'username': request.form.get('username')}})
    # print('updated class', updated_class)
    series_in_form = request.form.getlist('series')
    # print('series in form', series_in_form)
    # print('series id', series_doc)
    # Remove the class id from each of the series collection class_series array of objects classes arrays  
    series_collection.update_many({'_id': ObjectId(series_doc)}, {'$pull': {'class_series.$[].classes': class_id}}, upsert = False)
    # Loop through each of the series collection class_series array of objects classes arrays where the class_series ObjectId equals to id passed from the selected series option value
    for item in series_in_form:
        # Push the class_id to the Array
        series_collection.update_one({'_id': ObjectId(series_doc), 'class_series._id': ObjectId(item)}, { '$push': { 'class_series.$.classes': class_id} })
        # Check if the class_id was pushed to the array
        # array = series_collection.find_one({ '_id': ObjectId(series_doc) }, { 'class_series': {'$elemMatch': { '_id': ObjectId(item)}}})
        # print(array)
    return redirect(url_for('view_class', class_id = class_id ))

# DELETE CLASS FROM COLLECTION - remove()
@app.route('/delete_class/<class_id>/<series_doc>')
def delete_class(class_id, series_doc):
    deleted_class = classes_collection.remove({'_id': ObjectId(class_id)})
        # Remove the class id from each of the series collection class_series array of objects classes arrays when class is deleted from the collection
    series_collection.update_many({'_id': ObjectId(series_doc)}, {'$pull': {'class_series.$[].classes': class_id}}, upsert = False)
    # print(deleted_class)
    return redirect(url_for('classes',
                               title = 'Classes'))

# DUPLICATE CLASS -> to edit
@app.route('/copy_class/<class_id>')
def copy_class(class_id):
    copy_this  = classes_collection.find_one({'_id': ObjectId(class_id)})
    # Create a postfix (copy) for the class_name
    name = copy_this['class_name']
    postfix = '(copy)'
    edit_name = ''.join((name, postfix))
   # print("name", name)
    
    # Remove _id field from copy_this class document
    del copy_this['_id']
    # print('copy', copy_this)
     
    duplicated = classes_collection.insert_one(copy_this)
    duplicate = duplicated.inserted_id
    # print('new insert', duplicate)
    remove_name_and_logs = classes_collection.update_one({'_id': ObjectId(duplicate)}, { '$set': { 'class_name': edit_name, 'logs': [] }})
    # print('modified', remove_name_and_logs )
    return redirect(url_for('edit_class', title="Edit Class(copy)", class_id = duplicate))
    # Get the class and populate the form with some additional information - add (copy) in name value 

###################################### Handling Logs in Class / CRUD #################################

# ADD LOG - html/ form
@app.route('/add_log/<class_id>/<username>')
def add_log(class_id, username):
    # print(class_id)
    return render_template('addLog.html', class_id = class_id, username = username)
                 
# INSERT LOG TO CLASS - update_one(), $addToSet{}
@app.route('/insert_log/<class_id>', methods=['POST'])
def insert_log(class_id):
    new_log = {
        '_id': ObjectId(),
        'log_date': request.form.get('log_date'),
        'log_text': request.form.get('log_text'),
        'log_tag': request.form.get('log_tag')  
	}
    inserted_log = classes_collection.update_one({'_id': ObjectId(class_id)}, { '$addToSet' :{ 'logs': new_log}})
    # print(inserted_log)
    return redirect(url_for('view_class', class_id = class_id))

# EDIT LOG IN CLASS - html/ form - find_one(), $elemMatch{} 
@app.route('/edit_log/<class_id>/<log_id>', methods=['GET', 'POST'])
def edit_log(class_id, log_id):
    # print(log_id)
    this_log = classes_collection.find_one({'_id': ObjectId(class_id)}, {'logs': {"$elemMatch" : {'_id': ObjectId(log_id)}}})
    # print(this_log)
    return render_template('editLog.html', title='Edit log', this_log = this_log, class_id = class_id, log_id = log_id)

# UPDATE LOG IN CLASS AFTER EDIT - update_one(), $set{}
@app.route('/update_log/<class_id>/<log_id>', methods=['POST'])           
def update_log(class_id, log_id):
    update_log = classes_collection.update_one({'_id': ObjectId(class_id), 'logs._id': ObjectId(log_id)}, {'$set': {
        'logs.$.log_date': request.form.get('log_date'),
        'logs.$.log_text': request.form.get('log_text'),
        'logs.$.log_tag': request.form.get('log_tag')
    }})
    # print(update_log)
    return redirect(url_for('view_class', class_id = class_id))

# DELETE LOG FROM CLASS - update_one(), $pull{}
@app.route('/delete_log/<class_id>/<log_id>')           
def delete_log(class_id, log_id):
    deleted_log = classes_collection.update_one({'_id': ObjectId(class_id)}, {'$pull': { 'logs': {'_id': ObjectId(log_id)}}} )
    # print(deleted_log)
    return redirect(url_for('view_class', class_id = class_id))


###################################### Handling Exercises / CRUD #################################

# ADD EXERCISE - html/ form
@app.route('/add_exercise/<class_id>')
def add_exercise(class_id):
    return render_template('addExercise.html', title='New exercise', class_id=class_id)

# INSERT EXERCISE TO CLASS - update_one(), $addToSet{}
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
    # print(inserted_exercise)
    return redirect(url_for('view_class', class_id=class_id))

# EDIT EXERCISE - html/ form
@app.route('/edit_exercise/<class_id>/<exercise_id>', methods=['GET','POST'])
def edit_exercise(class_id, exercise_id):
    # print(exercise_id)
    this_exercise = classes_collection.find_one({'_id': ObjectId(class_id)}, {'exercises': {"$elemMatch" : {'_id': ObjectId(exercise_id)}}})
    # print(this_exercise)
    return render_template('editExercise.html', title='Edit exercise', this_exercise = this_exercise, class_id = class_id, exercise_id = exercise_id)

# UPDATE EXERCISE AFTER EDITING - update_one(), $set{}
@app.route('/update_exercise/<class_id>/<exercise_id>', methods=['POST'])
def update_exercise(class_id, exercise_id):
    # print(exercise_id)
    # updates the exercise entry in class - to tackle the issue of updating sub-documents in arrays:
    # https://stackoverflow.com/questions/36841911/mongodb-update-complex-document?noredirect=1&lq=1
    # provided the information I needed to formulate the correct syntax
    updated_exercise = classes_collection.update_one(
        {'_id': ObjectId(class_id), 'exercises._id': ObjectId(exercise_id)}, {'$set': {
        'exercises.$.exercise_name': request.form.get('exercise_name'),
        'exercises.$.exercise_description': request.form.get('exercise_description'),
        'exercises.$.exercise_comment': request.form.get('exercise_comment'),
        'exercises.$.exercise_aim': request.form.get('exercise_aim')}})
    # print(updated_exercise)
    return redirect(url_for('view_class', class_id=class_id))

# DELETE EXERCISE IN CLASS - update_one(), $pull{}
@app.route('/delete_exercise')
def delete_exercise():
    deleted_exercise = classes_collection.update_one({'_id': ObjectId(class_id)}, {'$pull': { 'exercises': {'_id': ObjectId(exercise_id)}}} )
    return redirect(url_for('view_class'))


######################################  Handling Music Tracks in exercises/ CRUD 

 # ADD MUSIC TRACK - html/ form
@app.route('/add_track/<class_id>/<exercise_id>')
def add_track(class_id, exercise_id):
    # print(class_id)
    # print(exercise_id)
    return render_template('addTrack.html', title="Music Track", class_id = class_id, exercise_id = exercise_id)

# INSERT NEW TRACK TO EXERCISE - update_one(), $addToSet{}
@app.route('/insert_track/<class_id>/<exercise_id>', methods=['POST'])
def insert_track(class_id, exercise_id):
    new_track = {
        '_id': ObjectId(),
        'track_title': request.form.get('track_title'),
        'track_link': request.form.get('track_link'),
        'track_comment': request.form.get('track_comment')
	}
    inserted_track = classes_collection.update_one({'_id': ObjectId(class_id), 'exercises._id':ObjectId(exercise_id)}, { '$addToSet': {'exercises.$.tracks' : new_track}})
    return redirect(url_for('view_class', class_id = class_id))

# DELETE MUSIC TRACK FROM EXERCISE- update_one(), $pull{} 
@app.route('/delete_track/<class_id>/<exercise_id>/<track_id>')
def delete_track(class_id, exercise_id, track_id):
    deleted_track = classes_collection.update_one({'_id': ObjectId(class_id), 'exercises._id':ObjectId(exercise_id)}, {'$pull': { 'exercises.$.tracks' : { '_id': ObjectId(track_id)}}})
    return redirect(url_for('view_class', class_id = class_id))


##################################### Handling Video Links in exercises/ CRUD 

# ADD VIDEO LINK - html/ form
@app.route('/add_link/<class_id>/<exercise_id>')
def add_link(class_id, exercise_id):
    return render_template('addLink.html', title="Video link", class_id = class_id, exercise_id = exercise_id)

# INSERT NEW VIDEO LINK TO EXERCISE - update_one(), $addToSet{}
@app.route('/insert_link/<class_id>/<exercise_id>', methods=['POST'])
def insert_link(class_id, exercise_id):
    new_link = {
        '_id': ObjectId(),
        'video_title': request.form.get('video_title'),
        'video_link': request.form.get('video_link'),
        'video_comment': request.form.get('video_comment')
	}
    inserted_link = classes_collection.update_one({'_id': ObjectId(class_id), 'exercises._id':ObjectId(exercise_id)}, { '$addToSet': {'exercises.$.links' : new_link}})
    return redirect(url_for('view_class', class_id = class_id))

# DELETE VIDEO LINK FORM EXERCISE - update_one(), $pull{} 
@app.route('/delete_link/<class_id>/<exercise_id>/<link_id>')
def delete_link(class_id, exercise_id, link_id):
    deleted_link = classes_collection.update_one({'_id': ObjectId(class_id), 'exercises._id':ObjectId(exercise_id)}, {'$pull': { 'exercises.$.links' : { '_id': ObjectId(link_id)}}})
    return redirect(url_for('view_class', class_id = class_id))


###################################### Handling Class Series / CRUD #################################

# VIEW CLASS SERIES - html
@app.route('/series')           
def series():
    # Check if user is logged in
    if 'user' in session:
        # If so get the user classes and pass them to a template
        user_in_db = users_collection.find_one({'username': session['user']})
        username = session['user']
        all_series = series_collection.find_one({'username': username})
        # print('all series', all_series)
        # print(username)
       # print(user_in_db)
        return render_template('series.html',
                               title = 'Series', 
                               username = username,
                               all_series = all_series)
    else:
    	flash("You must be logged in!")
    	return redirect(url_for('index'))
           
# VIEW CLASSES IN SERIES - html
@app.route('/view_classes_in_series/<username>/<series_id>/<series_doc>')           
def view_classes_in_series(username, series_id, series_doc):
    series = series_collection.find_one({'username': username})
    # Find specific serial (with _id: series_id) in series document (with _id: series_doc)
    serial = series_collection.find_one({ '_id': ObjectId(series_doc) }, { 'class_series': {'$elemMatch': { '_id': ObjectId(series_id)}}})
    # print('serial', serial)
    serial_name = serial
    # print('serial name', serial_name)
    # Find all classes of the user
    all_classes = classes_collection.find({'username': username})
    # print(type(all_classes))
    # print('all classes', all_classes)
     
    return render_template('view_classes_in_series.html', serial = serial, serial_name = serial_name, all_classes = all_classes, username = username, series = series)

# VIEW CLASSES IN None SERIES - None ROUTE

# ADD NEW CLASS SERIES - html/ form
@app.route('/add_series')
def add_series():
    username = session['user']
    user_id = users_collection.find_one({'username': session['user']}, {'_id': 1})
    # print(user_id)
    # This checks if the user already has a document in series collection, if not a document will be added.
    # https://stackoverflow.com/questions/25163658/mongodb-return-true-if-document-exists: answer by Xavier Guihot led to the right path with this.
    if series_collection.count_documents({'username': session['user']}, limit = 1) ==0:
        new_user_document = {
            'user_id': ObjectId(user_id),
            'username': username,
            'class_series': []
            }
        
        inserted_document = series_collection.insert_one(new_user_document)
        series_id = inserted_document.inserted_id
    return render_template('addSeries.html', title="Add Series", user_id = user_id, username = username)

# INSERT NEW SERIES OBJECT TO class_series ARRAY  - update_one(), $addToSet{}
@app.route('/insert_series/<username>', methods=['GET', 'POST'])
def insert_series(username):
    new_series_item = {
        '_id': ObjectId(),
        'series_name': request.form.get('series_name'),
        'series_description': request.form.get('series_description'),
        'classes': []
        }
    inserted_item = series_collection.update_one({'username': username}, { '$addToSet' :{ 'class_series': new_series_item}})
    # print(inserted_item)
    return redirect(url_for('series', title='Series', username=username ))
    
# EDIT SERIES IN class_series ARRAY - find_one(), $elemMatch{}
@app.route('/edit_series/<series_doc>/<series_id>', methods=['GET', 'POST'])
def edit_series(series_doc, series_id):
    this_series = series_collection.find_one({'_id': ObjectId(series_doc)}, { 'class_series' : {'$elemMatch': { '_id': ObjectId(series_id)}}})
    return render_template('editSeries.html', title='Edit series', this_series = this_series, series_doc=series_doc, series_id = series_id)

# UPDATE SERIES IN class_series ARRAY AND UPDATE THE SERIES IN series[] IN CLASSES - update_one(), $set{} and update_many(), $set{}
@app.route('/update_series/<series_doc>/<series_id>', methods=['GET', 'POST'])
def update_series(series_doc, series_id):
    
    updated_series = series_collection.update_one(
        {'_id': ObjectId(series_doc), 'class_series._id': ObjectId(series_id)}, {'$set' : {
            'class_series.$.series_name' : request.form.get('series_name'),
            'class_series.$.series_description': request.form.get('series_description')
        }})
    # update the series in classes as well!!
    # update series in classes
    # print(updated_series)
    return redirect(url_for('series'))

# DELETE SERIES FROM class_series ARRAY AND series[] IN CLASSES - update_one(), $pull{}
@app.route('/delete_series/<series_id>')
def delete_series(series_doc, series_id):
    deleted_series = series_collection.update_one({'_id': ObjectId(series_doc)}, { '$pull' : { 'class_series' : {'_id': ObjectId(series_id)}}} )
    # print(deleted_series)
    return redirect(url_for('series'))


if __name__ == '__main__': 

   app.run(host=os.environ.get('IP'),             
                                                  
      port=int(os.environ.get('PORT', 5000)),
      debug=True)           