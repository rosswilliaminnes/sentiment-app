from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

'''note sqllite is for an example, for larger data sets you need
postgre or mysql, you wull need to import more dependencies to connect!'''

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# now connect, could be local or remote (cloud!)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"# go to Connection URI Format sql alchemy' see examples for mysql postgres etc

'''note in the above the number of slashes matter 3 for relative path
and 4 for absolute

to activate in the directory in terminal type python:

>>> from app2 import db
>>> db.create_all()

then you should see the file pop un in the directory

'''

db = SQLAlchemy(app) # intialize the connection

class User(db.Model): # class needs to inherit from the db.model
    # create columns see sql-alcehmy for column types
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)

    # create a table with 4 columns

@app.route('/<name>/<location>') # adds data to db
def index(name,location):
    user = User(name=name,location=location)
    db.session.add(user) # add to db
    db.session.commit() # commits to db

    return '<h1>Added New User!</h1>'


@app.route('/<name>') # get the db data
def get_user(name):
    user = User.query.filter_by(name=name).first()
    return f'the user is located in: { user.location}'



if __name__=='__main__':
    	app.run(debug=True)
    

