import os                  
from flask import Flask, render_template, url_for    

app = Flask(__name__)      

data = [
    {'class_name': 'Monday Groove',
     'class_description': 'Let it loose and sweat it out',
     'main_element': 'Shaky shake moves',
     'log_date': 'March 7, 2020'},
    {'class_name': 'Tuesday Tango',
     'class_description': 'Get down and dirty',
     'main_element': 'Roses and shiny shoes',
     'log_date': 'March 8, 2020'},
    {'class_name': 'Monday Funk',
     'class_description': 'Funky monkeys monday feast',
     'main_element': 'The boom start for your week',
     'log_date': 'March 14, 2020'}
]

series_data = [
    {'series_name': 'Funky mondays',
     'class_name': 'Monday Groove',
     'class_description': 'Let it loose and sweat it out'
    },
    {'series_name': 'Funky mondays',
     'class_name': 'Monday funk',
     'class_description': 'Funky monkeys monday feast'}
]


@app.route('/')
@app.route('/home')           
def home():             
    return render_template('home.html')

@app.route('/about')           
def about():             
    return render_template('about.html', title='About')

@app.route('/classes')           
def classes():             
    return render_template('classes.html', title='Classes', classes=data)

@app.route('/series')           
def series():             
    return render_template('series.html', title='Series', series=series_data)


if __name__ == '__main__': 

   app.run(host=os.environ.get('IP'),             
                                                  
      port=int(os.environ.get('PORT', 5000)),
      debug=True)           