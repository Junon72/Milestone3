
# Classapp - Data Centric Development Milestone Project 3

## Online Dance Class Archiving Tool For Dance Teachers

Heroku App: https://flask-classapp.herokuapp.com/

Heroku git: https://git.heroku.com/flask-classapp.git

GitHub: https://github.com/Junon72/Milestone3

The project was created as Milestone project for the Data Centric Development module in  Code Institute run Full Stack Web Development course program.

---

# Project brief

The project is following my own desire to bring about a digital tool for the community I my self belong to, the dance teachers. The project is built using data-driven application technologies I have learned about on the course module. Classapp intends to provide a mobile and easy tool to plan, store and manage dance classes, in a digital form which is accessible where ever they might be teaching.

## Context

>The idea for the application is direct response to my own experiences as a dance teacher which I believe I share with many other in this occupation. Classapp is designed for dance teachers, to design, save and archive their dance classes.

> There are dozens of different dance style and genres taught in most diverse settings all over the world. Be it street dance,folk, classical, contemporary, tap, ballroom to start by mentioning just a few, each class is a result of a dedicated work by a dance teacher. A dance class is just the tangible and experiential manifestation of the skill and creativity of the dance teacher front of the class. Much of the teachers work is hidden. Making, or designing classes happens outside the teaching itself, competing for time from other necessary tasks that come with the job.

>Dance class material is often tailored for specific occasions with their own specific goals and needs. Teachers have to keep in mind the level of the students taking the class, wishes of the organizations where they teach or needs of educational institutions curriculums when designing classes or series of classes. For example, designing a series of dance classes for higher educational institutions, the classes should provide thematically coherent experience for the dance students, while filling all kinds of other equally important objectives and requirements set by the institution. Teaching in an open studio, in a dance company, for amateurs, for children or for professionals have all very different kinds of implications and requirements.

>Class material tends to accumulate with time and good material and well working classes can get lost and forgotten. Information and valuable insights, such as the first hand experiences with the students, tend to vanish with the forgotten classes. Especially when working with groups of students in schools, in order to help the students improve over time, notes and remarks from the past are most useful resource of feedback. They are also good material for reflection and self assessment for teachers themselves, who often can only rely on their own judgement.

>Teachers time is often limited and the time for planning, personal improvement and developing new ideas is rarely paid. Sometimes, to come up with new material can be taxing and time consuming. Resorting to already tested material is often helpful and can be a huge time saver. For teachers own personal development it is important to change the habits every now and then and look for new perspectives and ideas. Revisiting past classes and notes is often a good point of departure when looking for new inspiration. It helps to recognize habitual patterns, find new angles and gain new insights. Building a comprehensive archive of classes can thus be a time saver, but also a source of inspiration, reflection and a valuable tool in maintaining alive relationship to teaching the art of dance.

## Project Overview

I considered following features essential for application to fulfill its purpose:

1. User can create his/ her own archive, which is accessible only for him /her

For this the user can:

a. create an account with a username and password

b. login with the username and password

2. User can create classes

Once a class is created user can:

a. view class

b. edit class

c. delete class

d. duplicate class

e. associate the class with class series user has created

f. de-associate the class with class series user has created

3. User can create exercises for a class

Once an exercise is created, user can:

a. view exercise

b. edit exercise

c. delete exercise

d. add and delete links to music tracks and videos

4. User can create logs for the classes

Once a log is created, user can:

a. view log

b. edit log

c. delete log

5. User can create series of classes for various purposes

Once a series is created, user can:

a. view series

b. view classes associated with the series

c. edit series

d. delete series

Classapp provides a mobile and easy tool to plan, store and manage dance classes, in a digital form which is accessible where ever they might be teaching.

# UX

## Who is this application for ?

### Possible users types

- A freelance teacher working with companies, schools and/or dance studios.
- A curriculum teacher in an educational institution/ permanent school staff.python3 app.py
- Recurring teacher in different educational institutions.
- Company teachers.
- Dance teacher, movement coach, body worker, gym teacher and so forth in any class or workshop setting.

### User stories

1. I really need a way to organize the class information so I can look at the classes I have taught, with my notes and logs to set sensible longer term goals for my students.

2. I would like to be able to recall some of my classes from the past, which would give me an idea how my class has evolved and what kind of information was produced and shared - a bit like a diary, but easier to use - to have some inspiration for new classes.

3. Would be great to have a videos from my classes at hand sometimes to refresh my memory and to see what could I do differently or better.

4. I would need a way to archive my classes and be able to write detailed logs so I can follow the progress of my students over time and share some insights with my colleagues.

5. It would be handy to be able to easily design a series of classes in advance for specific purposes, which I could then copy and modify depending where I am teaching. I am teaching a lot in different kinds of places, but I do not have time to always come up with a new plan, sometimes a little alteration to an old class is good enough, but after a while I'm getting confused which version I teaching.

6. I would like to be able to store my classes so that I can find the best fit in each situation, depending on the level of the people I will be teaching, or even the size of the studio or amount of the expected participants. For example, when I need to teach a class with small adjustments to the usual exercise material to accommodate some situations, like a very small studio.

7. It would be practical to have the associated music tracks and playlists with links stored with the classes and exercises and possibility to write remarks, such as, this track is good for a slower tempo, or this is good energetic music to pump up the class etc.

8. I really need a way to organize the class information so I can look at the classes I have taught, with my notes and logs to set sensible longer term goals for my students.

9. Would be really handy to be able to have like digital document, where I could put images and stuff together with my class and exercises, and everything. I could then show thing like, how is the anatomy or demonstrate what I mean with other kinds of media etc. But all in a same place... and that is easy to take to the class.

10. I would like to have a tool that would structure and unify my class designs to make it easier to visit them later - digital would be great so I don’t need to be guessing what I was writing. Actually, something that would help notating my classes would be amazing.



## Technologies Used

Technologies used building this project include,

- [VSCode](https://code.visualstudio.com/ "VSCode") IDE, is a source-code editor developed by Microsoft for Windows, Linux and macOS.
- [Balsamiq Mockups3](https://balsamiq.com/wireframes/desktop/) is a user interface design tool for creating wireframes.
- [Bootstrap](https://getbootstrap.com/ "Bootstrap") is a free and open-source CSS framework directed at responsive, mobile-first front-end web development.
- [Bson](http://bsonspec.org/ "Bson") is a computer data interchange format in JSON-like document that MongoDB uses when storing documents in collections.
- [Chrome Developer Tool](https://developers.google.com/web/tools/chrome-devtools "Chrome Developer Tool")s is a set of web developer tools built directly into the Google Chrome browser that help allow web developers to test and debug their code.
- [CSS3](https://developer.mozilla.org/en-US/docs/Archive/CSS3 "CSS3") is a style sheet language used for describing the presentation of a document written in a markup language like HTML.
- [Config](https://pypi.org/project/config/) is a module that allows a hierarchical configuration schemes within Python projects.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/ "Flask") is a micro web framework written in
- [Flask Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/) is a Flask extension that provides bcrypt hashing utilities for your application.
- [Flask PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) is a bridging tool between Flask and PyMongo.
- [Flask Session](https://pythonhosted.org/Flask-Session/) is an extension for Flask that adds support for Server-side Session to your application.
- [Git](https://git-scm.com/ "Git") is a distributed version-control system for tracking changes in source code during software development.
- [GitHub](https://github.com/ "GitHub") is a Web-based hosting service for version control using Git.
- [GitIgnore ](https://www.gitignore.io/ "GitIgnore ")is a free web service that help create .gitignore templates.
- [Gunicorn](https://pypi.org/project/gunicorn/) takes care of everything which happens in-between the web server and your web application, making sure that web servers and python web applications can talk to each other.
- [Heroku](https://www.heroku.com/ "Heroku") is a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.
- [HTML5](https://html.com/html5/) is code that describes web pages.
- [JavaScript](https://www.javascript.com/ "JavaScript") is an interpreted programming language that conforms to the ECMAScript specifications and most commonly used scripting language for Web pages.
- [Jinja2](http://jinja.pocoo.org/ "Jinja2") is a web template engine for the Python programming language.
- [Python 3.7.6](https://www.python.org/ "Python 3.4.3") is an interpreted, high-level, general-purpose programming language.
- [PyMongo](https://api.mongodb.com/python/current/ "PyMongo") is a distribution tool for interacting with MongoDB database from Python.
- [Slack](https://slack.com/intl/en-nl/lp/three?utm_medium=ppc&utm_source=google&utm_campaign=d_ppc_google_western-europe_en_brand-hv&utm_term=slack&ds_rl=1249094&gclid=Cj0KCQiAs67yBRC7ARIsAF49CdWe8odCtapVb73H6AUvEA8OADzSxxCqgfdc43zlDNxxb3EX22dAhHgaAredEALw_wcB&gclsrc=aw.ds) is a cloud-based proprietary instant messaging platform.
- [Werkzeug](https://palletsprojects.com/p/werkzeug/ "Werkzeug") is a comprehensive WSGI web application library, used to build all sorts of end user applications such as blogs, wikis, or bulletin boards, not to mention user login and registration handling.

## Setting up IDE

### Working with VSCode and Python

The project was developed using [VSCode IDE](https://code.visualstudio.com/ "VSCode IDE") with Mac OS High Sierra operating system.
For the version control, the code was pushed to local git repository and then to [GitHub](https://github.com/ "GitHub") repository. The application was then autodeployed through [Heroku](https://www.heroku.com "Heroku") from the GItHub Master.

To work with python, Python3 library was first installed locally to the root directory with [Homebrew package manager](https://brew.sh/ "Homebrew package manager"). [Install Homebrew](https://brew.sh/#install "Install Homebrew") has instructions how to install brew to Mac.

To check if and which versio of Python you have installed (Mac comes Python2 preinstalled) globally, you can open the Terminal and type:

`$ python --version`  # this will give you the version of python2

 To see if you have Python3 installed, type:

 `$ python3 --version`

 I wrote the application using Python3.7.6

It is good to aknowledge the fact that [from 2020 January on, Python2 does not recieve further official support](https://wiki.python.org/moin/Python2orPython3 "from 2020 January on, Python2 does not recieve further official support"). Here you can find instructions [how to install the latest version of Python on your Mac](https://docs.python-guide.org/starting/install3/osx/ "how to install the latest version of Python, or to upgrade to Python3").

VSCode uses Python interpreter extensions to read Python code. Extensions include helpful features for the developers, such as [editing helpers, debugging, linting and testing.](https://code.visualstudio.com/docs/python/python-tutorial "editing helpers, debugging and linting.")

Application uses Python libraries and package modules to accomplish the needed functions. After setting up the IDE to your liking, and creating your working directory, but before starting to code and using Python modules, it is important to isolate your development environment. Otherwise, there might rise conflicts between different package versions you might use for different Python projects. Python3 comes with a build in tool 'venv' to create a [virtual environments](https://realpython.com/python-virtual-environments-a-primer/ "virtual environments") for this purpose.

To create a virtual environment in VSCode on Mac, in VSCode Terminal type:

`$ python3 -m .venv <file_name>`

This will create a virtual environment folder to the root directory of your project.
Often the files are named either env, venv or .venv.

The folder contains the following sub-folders:

- bin: files that interact with the virtual environment
- include: C headers that compile the Python packages
- lib: a copy of the Python version along with a site-packages folder where each dependency is installed

To activate the virtual environment, type:

`$ source <name_of_the_venv_file>/bin/activate`

This will activate the environment. After activation you will see the environment name in brackets front of the command line in which context the system now operates.

`(<name_of_the_venv_file>) $`

Now the Python version is run from the virtual environment file, rather than from the global install and the Python packages imported using pip3 are isolated to the this environment only. From Python3.6 on this is the recommended method of using virtual environments.

### Testing Python installation

To test the Python installation and the environment path:

1. Create a test.py file in root directory
2. In test.py file write:

```python
import sys
    # this line prints if python is installed correctly
    def greet(greetings_to):
    greeting = 'Hello, { }'.format(greetings_to)
    return greeting

    # this line will print out the current python path 
    # and the version of the python print(sys.executable)
    print(greet('World!'))
```

To run the file, type:

`$ python3 test.py`

You should see the following output in your terminal:

```bash
Hello, World!
/<name_of_the_workspace>/<name_of_the_venv_file>/bin/python3
```

*Test result: Passed**

- Python is installed and works correctly
- The code runs in virtual environment context

To exit the environment type:

`$ deactivate` which will return back to the 'system' context

You would want to do the development work in your virtual environment!

## Setting up git for version control and connecting to GitHub

For version control I have used GirHub open source version control system. You can alos yous Git or any other version control system provider. To make a GitHub account you can [follow the instructions here](https://help.github.com/en/github/getting-started-with-github).

Before establishing the connection to GitHub, I created a .gitignore with the help of [Gitignore](http://https://www.gitignore.io/ "gitignore") in order to avoid pushing Operating System, IDE, Programming language and virtual environment folders and files to the public domain. It also safer to put the configurations to a separate file from
the main Python file and add the file path to the .gitignore.

### Creating a local git repository

Initialize a local git and add the files the repository:

`(.venv) $ git init` # creates a git file for the project

`(.venv) $ git add .` # adds all the current files, excluding the files defined in .gitignore

`(.venv) $ git commit -m"Initial commit"` # commits the files into the local git repository`

I have installed VSCode GitHub extension, which makes committing changes slightly easier, by skipping username and password inquiry with each new commit.

### Create a new project in GitHub

In your GitHub account go to **Your repositories** view and create a new repository for the project by clicking the green button **New**. Name the repository to your liking following the instruction for the naming rules. Click **Create repository**. This will take you to **Quick setup** view, where you can find the push command **...or push an existing repository from the command line**. Copy the lines and paste them to your terminal. You will be asked your GitHub password to push the git commit to your GitHub repo.

### Create a new project through command line

You can also create a new repository through the command line.

`(.venv) $ echo "# <name_of_your_project>" >> README.md`

`(.venv) $ git init`

`(.venv) $ git add README.md`

`(.venv) $ git commit m-"Initial commit"`

`(.venv) $ git remote add origin https://github.com/<username>/<repository_name>.git`

`(.venv) $ git push -u origin master`

I have installed VSCode GitHub extension, which makes committing changes slightly easier, by skipping username and password inquiry with each new commit.

## Installing and testing Flask

To install Flask to your work environment, in Terminal type:

`(.venv) $ sudo pip3 install Flask`

*The system reports I am using older version of pip.*

```bash
WARNING: You are using pip version 19.2.3, however version 20.0.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```

*After upgrade I run the code again.*

**Testing:**

- To ensure the Flask is installed, type:

`(.venv) $ pip3 freeze --local`

This will tell which packages are currently installed.

*Test result: Passed**

- Terminal output reads.

```bash
Click==7.0
Flask==1.1.1
itsdangerous==1.1.0
Jinja2==2.11.1
MarkupSafe==1.1.1
Werkzeug==1.0.0
```

### Flask test script

In test.py I created a script to test the working of Flask in VSCode IDE.

```python
# Functionalities to import from modules
import os                   # Imports operating system dependent functionality.
from flask import Flask     # Imports Flask class from flask module.

app = Flask(__name__)       # An instance of Flask class construction.

# Route Decorator
@app.route('/')             # URL handled by main() route handler.
    def welcome():          # Defines a function that returns "Hello World".

    return "Welcome Flask!"

if __name__ == '__main__':  # tells the global namespace __name__ is set to equal "__main__"

    # If conditional statement is satisfied
    app.run(host=os.environ.get('IP'),  
        # launches the Flask built-in development web server and   
        # gets the IP Address from the operating system.
        port=int(os.environ.get('PORT', 5000)), 
        debug=True)
        # Gets PORT we want to open, which in this case is set to 5000.
        # Enable reloader and debugger by setting it to True, 
        # which is the recommended value for the development phase
```

Run the script:

`(.venv) $ python3 test.py`

Terminal output:

```bash
* Serving Flask app "test" (lazy loading)
* Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
* Debug mode: on
* Running on http://#.0.0.#:5000/ (Press CTRL+C to quit) - I have hide the actual IP address with #!!
* Restarting with stat
* Debugger is active!
* Debugger PIN: 263-007-180
```

Following the link (option + click) opens the browser and 'Welcome Flask" is rendered on the screen.

*Test result: Passed**

Now that I know flask is installed and works in the os as well, I created the actual application file app.py.
In the file I modified the message to Hello World!
I run app.py to confirm the code works proper.

### Testing the routes

I created a new route to Classes page to test the routing decorator function and html.

I get an endpoint error message, because the Classes page doesn't exist yet.

*Test result: Failed*
To fix the error I created Classes page and run app.py again.
In address bar I add /about after the IP to navigate to the Classes page.

*Test result: Passed**

- routes work
- html works

## Working with templates and Jinja2

The html pages are routed via app.py in this phase.
To test the rendering tool, import render_template from flask and implement it to your code.

*Test result: Passed**

- The pages are now rendered via app.py

To work with dynamic data, I created an array of dummy classes and connected the data to the Home page using Python Jinja template management engine.

Dummy data:

```python
data = [
    {'class_name': 'Monday Groove',
    'class_description': 'Let it loose and sweat it out',
    'main_element': 'Shaky shake moves',
    'log_date': 'March 7, 2020'},
    {'class_name': 'Tuesday Tango',
    'class_description': 'Get down and dirty',
    'main_element': 'Roses and shiny shoes',
    'log_date': 'March 8, 2020'}
    ]
```

*Test result: Passed**

- the data is rendered dynamically on the home page

After testing that the routing works, I added own html page for the links in 'head' section, the navigation, and the scripts section and moved the section content into their own page. I gave the navigation some styling and tested that the sections render correctly.

*Test result: Passed**

- the links, navigation and scripts work as they should

## url_for routing

To avoid hard coding of URLs in flask, the href links can be routed using url_for module of flask.
After changing the css routing, I created the actual webpages the user can navigate to from the navigation bar,
and changed the href paths to url_for routes.

The data will be added dynamically to the Classes and Series pages. The paths in decorator in app.py, needs to be updated.

Testing the navigation and the data rendering, I followed the navigation link to Classes and Series pages.

*Test Result Classes page: Passed**

- The dummy data renders as expected on the Classes page

*Test Result Series Page: Fail**

- Terminal output states.

```bash
jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'endfor'. Jinja was looking for the following tags:  'endblock'.
```

I created a dummy data for series and run the test again.

*Test Result: Passed**

- Also the Series dummy data renders correctly.

I tested the rest of the navigation links in the navigation bar.

*Navigation Test Result: All Passed**

- Navigation link is routed to the correct pages.
- The pages and page title render correctly.

## Displaying Classes on classes.html

To display the classes user has created I used Materialize collapsible element. I tested the page with the dummy data, before connecting the MongonDB database to the project.

*Test Result: Passed**

- Dummy data renders correctly on the dynamically created Materialize element.
- The Collapsible element opens and closes correctly

## MongoDB Atlas

### Getting the MongoDB working together with Python

The application uses MongoDB Atlas cloud storage for storing the user data. An additional distribution tool PyMongo is needed to access MongoDB database with Python.  

To install PyMongo, in Terminal type:

`(.venv) $ sudo pip3 install pymongo`

Make sure you are operating in virtual environment context!

Terminal output:

`Successfully installed pymongo-3.10.1`

You also need to install flask-pymongo to connect your MongoDB database with Flask application to perform CRUD operations.

To install flask-bymogo, in Terminal type:

`(.venv) $ sudo pip3 install flask_pymongo`

Terminal output:

`Successfully installed flask-pymongo-2.3.0`

To comply with the newest connection string used by MongoDB, you also must install dnspython module which is a DNS toolkit for Python

To install dnspython, in Terminal type:

`(.venv) $ sudo pip3 install dnspython`

Terminal output:

`Successfully installed dnspython-1.16.0`

### Connecting the application

To connect an application to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) database, first you need to be registered. For registration follow the steps provided on the free starter [registration pages](https://www.mongodb.com/cloud/atlas/register), for creating account and deployment follow the instruction on [Getting Started with Atlas pages](https://docs.atlas.mongodb.com/getting-started/).

MongoDB has a practical dashboard utility where the user can create databases, and manage document collections in them.
In MongoDB dashboard I created a new cluster and a project context for Classapp and added a new database.
In the database I then created a new collection 'clasess' and in the classes collection a new 'class' document.

```python
    _id:ObjectId("5e519eb9ba2dfb000006dfe1")
    class_name:"Monday Groove"
    class_description:"Let it loose and sweat it out!"
    main_elements:"Shaky shake moves"
    other_elements:"Shovel the toes, Slide with grace"
    playlist_title:"Billie Eilish"
    playlist_url:"https://www.youtube.com/watch?v=xNV38nq1fqc"
    class_notes:"This class makes you SWEAT, bring water and a towel"
    exercises:Array
        0:Object
            _id:ObjectId("5e51a370ba2dfb000006dfe6")
            exercise_name:"Get it going"
            exercise_description:"Wiggle the toes, while you touch your nose"
            exercise_comment:"Slow cooking makes the best stew"
            exercise_aim:"Gets your toes moving, while maintaining focus to that which is the ne..."
            tracks:Array
                0:Object
                    _id:ObjectId("5e51a3ebba2dfb000006dfe7")
                    track_title:"Billie Eilish/ Bad Guy"
                    track_link:"https://www.youtube.com/watch?v=DyDfgMOUjCI"
                    track_comment:"It ain't salsa, but... I like Billie Eilish, ok"
            links:Array
                0:Object
                    _id:ObjectId("5e51a454ba2dfb000006dfe8")
                    video_title:"Say salsa/ Quick Feet Studio"
                    video_link:"https://www.youtube.com/watch?v=vfpajx2uemE"
                    video_comment:"The Quick & Dirty Guide to Salsa, Part 1. All the lessons put together..."
    logs:Array
        0:Object
            _id:ObjectId("5e51a32dba2dfb000006dfe5")
            log_date:"07/01/2020"
            log_text:"Was wonderful class. Remember to start slow and ALWAYS smile"
            log_tag:"1st class for DanceFloor"
```

To connect to the database, in MongoDB in the application CONTEXT Classapp and in the Clusters view, select CONNECT.
This will pop up a dialogue. To test the connection choose the Connect With Mongo Shell option.
With Mongo Shell installed, choose the right hand side option, and copy the provided link.
Paste the link to the Terminal, and modify the username part as appropriate.
You will be asked to enter the password.

If the connection is successful, the terminal output should be something along the line:

```bash
Implicit session: session { "id" : UUID("dfie1392-7138-4662-9cf4-a271hf31f47f") }
MongoDB server version: 4.2.3
MongoDB Enterprise Cluster2-shard-0:PRIMARY>
```

### Preparing VSCode for MongoDB

To connect ot the cluster you need to have installed MongoDB Tap into your computer.
This you can do with Homebrew. In terminal write:

`$ brew tap mongodb/brew`

Then pour from the tap to install the latest MongoDB Community edition.

`$ brew install mongo-community`

To connect to the server from elswhere in your network you can install MongoDB Shell.

`$ brew install mongodb/brew/mongodb-community-shell`

To start teh service type.

`$ brew services start mongodB`

### Connecting to MonogoDB Atlas from IDE terminal

In terminal we can now connect to to MongoDB by typing.

```bash
$ mongo  'mongodb+srv://<db_user>:<db_password>@cluster2-8wde6.mongodb.net/<your_database>?retryWrites=true&w=majority'
```

(In place of db_user, use your own MongoDB username, in place of db_password, use your password and in place of
your_database, use the name of your database)

This should give a following terminal output:

```bash
MongoDB shell version v4.2.2
connecting to: mongodb://cluster2-shard-00-02-8wde6.mongodb.net:27017
Implicit session: session { "id" : UUID("421af287-fa81-4bcf-a827-4f2a91525585") }
MongoDB server version: 4.2.5
MongoDB Enterprise Cluster2-shard-0:PRIMARY> 
```

To test the connection to the cluster type:

`$ show collections`

This gives the name of the collection in the cluster. Mine at this point is:

`classes`

*Test result: Passed**

- Mongo Shell connected to the Classapp database and found the current collections in it.

### Pymongo

To be able to programmatically do CRUD operations from your Flask application you need to install dnspython and Pymongo library.

`$ sudo pip3 install dnspython`

And finally.

`$ sudo pip3 install pymongo`

To test that the libraries that are now installed type.

`$ pip3 freeze`

*Test result: Passed**

- dns and pymongo libraries were installed.

### Flask-Pymongo

To connect to the MongoDB with Flask application and perform CRUD operations you need to install also Flask-Pymongo.

`$ sudo pip3 install flask_pymongo`

**!! SECURITY !!**

It is important to make sure that the connection configurations with passwords and other connecions strings stay safely hidden from the user.
I put the MongoDB URI with the username and the password into a separate environment file config.py and added it to the .gitignore. The project uses Config module for the configuration schema.

To install Config, in Terminal type:

`(.venv) $ sudo pip3 install config`

Create config.py file and add the configuration vars into the file:

```python
# os is used to to link the config.py and app.py
import os
# the vars are stored into a class object
class Config(object):

# General config
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')
FLASK_APP = os.environ.get('FLASK_APP')

# Database config
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://<db_user>:<db_password>@cluster2-8wde6.mongodb.net/<database_name>?retryWrites=true&w=majority')
MONGO_DBNAME = os.environ.get('<database_name>')
```

To test Flask connection to the MongoDB I used following test in test.py environment:

```python
import os
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, url_for
from config import Config
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object(Config)

# MongoDB name
app.config['MONGO_DBNAME'] = 'classapp'
MongoDB URI / Assign db
client = MongoClient(Config.MONGO_URI)
db = client.classapp


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
```

*Test result: Passed**

- Mongo is connected!

### Libraries

By now the following libraries should be added to the app.py file:

```python
import os
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
```

### Adding to the collections

To add collections to your database, in MongoDB dashboard click on **Collections**.
Then add collection name and click **Create**.

## Heroku

### Heroku and VSCode

To use Heroku with VSCode, I installed Heroku and Heroku-cli extensions from the VSCode market place.
Heroku has its own version control system. You can also connect you GitHub repository to your Heroku application. You can find the instruction how to do that at the end of this Heroku deployment section. Connecting at later state is best to do after the actual deployment, otherwise the Heroku might mis some essential configurations to run the application. The following steps are for Mac OS and VSCode with GitHub version control, Heroku and Heroku-cli set up.

### Deployment procedure for [Heroku](https://www.heroku.com/ "Heroku") hosting site

To begin with deployment on Heroku go to [Heroku landing page](https://www.heroku.com/ "Heroku"). There you will find an option to either Sign in or Sign up.  If you have not signed up for Heroku platform before you can start here, otherwise you can continue from Login.

#### Signing up to Heroku

- On [Heroku](https://www.heroku.com/ "Heroku") Sign up.
- Complete the form presented to you. In at the ned ogf the form, in Primary development language dropdown, select Python.
- After submitting the form you will receive a confirmation email asking you to confirm you newly created Heroku account. (It can take some time before the email arrives - up to 15min.)
- To activate the account, follow the link and  after creating a password click the button to proceed.

#### Login to Heroku

- On your dashboard, select **New** and **Create new app**
- Create **App name**, then **Choose your region**, and finally click **Create app**

-Before deploying you project , you have to have created requirements.txt file and Procfile file in you project DOM. Also the Config variables have to be set*

Now that you have created Heroku space for you application, in your IDE (I used VSCode for this project) prepare you project for the deployment.

### Connecting to Heroku and creating the app

After login you can directly connect to Heroku by typing.

`$ heroku apps`

*Test result: passed**

- Terminal output is my email address I have created the Heroku account with followed by 'Apps', and list of applications in my Heroku account.

Next, create the app in Heroku by typing.

`$ heroku create <app_name>` using the name of your application in place of app_name.

*Test result: passed**

```bash
Creating ⬢ flask-classapp... done
     https://flask-classapp.herokuapp.com/ | https://git.heroku.com/flask-classapp.git
```

- Application was created in Heroku

Test the operation by typing

`$ git remote -v`

This will add a new remote.

*Test result: passed**

```bash
heroku  https://git.heroku.com/flask-classapp.git (fetch)
heroku  https://git.heroku.com/flask-classapp.git (push)
origin  https://github.com/Junon72/Milestone3.git (fetch)
origin  https://github.com/Junon72/Milestone3.git (push)
```

- The application is connected to two remotes now.

Since I have set my VSCode working environment to use GitHub for version control it is added automatically.
Otherwise you will see only Heroku git address.

### Adding Procfile and requirements file

Before adding the Procfile you need to install gunicorn.

`$ pip3 install gunicorn`

Then create Procfile in your .venv base base directory (just Procfile, with no extension!).
This specifies for Heroku the commands that are executed by the application on startup.
In Procfile type.

`web gunicorn <your_python_file_name>:app`

(your_python_file_name is written without the .py extension in this case!)

After creating Procfile, create the requirements.txt file to your .venv base directory.

`$ pip3 freeze --local > requirements.txt`

### Commit and open the application

At this point commit and push the application to Heroku.

`$ git add .`

`$ git commit -m"your_commit_message"`

`$ git push heroku master`

You should see now Heroku deploying the app and verifying it.

*Test result: passed**

```shell
remote: Verifying deploy...
(... a long list of lines explaining the stages in Heroku deployment process ...)
...done.
address_to_heroku_application_git
* [new branch]      master -> master
```

- Deployment is verified

### Open the application and finish the configuration in Heroku

After this you can go to your Heroku account and open your application. On right upper corner you find a button **Open app**. Click the button.

*Test result: passed**

- The application opens in a browser window.
- In **Overview** I have a message Build Succeeded and confirmation that the application is deployed and running.

To finish with Heroku configuration, in Heroku dashboard go to **Settings**. In settings you find a button **Reveal Config Vars**. Click the button.

On the **Config Vars** field **KEY** add IP and set the **VALUE** to 0.0.0.0.
Add another key value pair and set the key as PORT and value as 5000.

### Connecting Heroku and GitHub after deployment

You can do this from your Heroku application dashboard **Deploy**. There you find **Deployment method** section and an option **Connect to GitHub**. When selected, Heroku asks you to **Search** and define the path to your GitHub repository. **Connect** and your GitHub and Heroku version controls are now linked.
