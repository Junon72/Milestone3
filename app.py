import os                  
from flask import Flask, render_template    

app = Flask(__name__)      

data = [
    {'class_name': 'Monday Groove',
     'class_description': 'Let it loose and sweat it out',
     'main_element': 'Shakey shake moves',
     'log_date': 'March 7, 2020'},
    {'class_name': 'Tuesday Tango',
     'class_description': 'Get down and dirty',
     'main_element': 'Roses and shiny shoes',
     'log_date': 'March 8, 2020'}
]


@app.route('/')
@app.route('/home')           
def home():             
    return render_template('home.html', classes=data)

@app.route('/about')           
def about():             
    return render_template('about.html')



if __name__ == '__main__': 

   app.run(host=os.environ.get('IP'),             
                                                  
      port=int(os.environ.get('PORT', 5000)),
      debug=True)           