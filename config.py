import os
class Config(object):
    
    # General config
    SECRET_KEY = os.environ.get('SECRET_KEY', '5143fye2f6f15p6f77dudf0f355b20c6')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    
    # Database config
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://userMe72:U5erM3@cluster2-8wde6.mongodb.net/classapp?retryWrites=true&w=majority')
    MONGO_DBNAME = os.environ.get('classapp')