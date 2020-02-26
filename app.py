import os
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, url_for, session, flash
from config import Config
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__) 
app.config.from_object(Config)     


mongo = PyMongo(app)

# Collections

users_collection = mongo.db.users
classes_collection = mongo.db.classes

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
			return redirect(url_for('classes', user=user_in_db['username']))
	else:
		# Render the page for user to be able to log in
		return render_template("index.html", title="Login", current_users=list(users_collection.find()))

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
			return redirect(url_for('classes', user=user_in_db['username']))
			
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
					return redirect(url_for('index', user=user_in_db['username']))
				else:
					flash("There was a problem registering you, please try again")
					return redirect(url_for('register'))

		else:
			flash("The passwords are not identical!")
			return redirect(url_for('register'))
		
	return render_template('register.html', title='Register')

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
        user = user_in_db
        print(user)
        classes=classes_collection.find({'username': user})
        print(classes)
        for one in classes:           
        	print(one)
        return render_template('classes.html', title='Classes', classes=classes_collection.find({'username': user}))
    else:
    	flash("You must be logged in!")
    	return redirect(url_for('index'))


@app.route('/series')           
def series():             
    return render_template('series.html', title='Series')




if __name__ == '__main__': 

   app.run(host=os.environ.get('IP'),             
                                                  
      port=int(os.environ.get('PORT', 5000)),
      debug=True)           