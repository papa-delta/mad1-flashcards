from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#create a Flask Instance
app=Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3'

#Initialize the database
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

#create Model
class cards(db.Model):
    cid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    obverse=db.Column(db.String(100), nullable=False)
    reverse=db.Column(db.String(100), nullable=False)
    score=db.Column(db.Integer,default=1)

class decks(db.Model):
	did=db.Column(db.Integer,primary_key=True,autoincrement=True)
	deck_name=db.Column(db.String(100), nullable=False, unique=True)
	cid=db.Column(db.String(100), nullable=True)
	deck_score=db.Column(db.Integer)
	deck_description=db.Column(db.String(100))
	last_reviewed=db.Column(db.String(10))


class users(db.Model):
    uid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    decks_owned=db.Column(db.Integer, db.ForeignKey('decks.did'),nullable=True)
    username=db.Column(db.String(10),nullable=False)
    name=db.Column(db.String(100))
    

#db.create_all()
