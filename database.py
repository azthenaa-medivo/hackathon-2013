import handler

from google.appengine.ext import db

class Discussion(db.Model):
	title = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)

class Proposition(db.Model):
	numero = db.IntegerProperty(required = True)
	text = db.TextProperty(required=True)
	
class Survey(db.Model):
	username = db.StringProperty(required=True)
	posted = db.DateTimeProperty(auto_now_add=True)
	question = db.TextProperty(required=True)
	result = db.ReferenceProperty(Proposition,required=False)
	
class Reponse(db.Model):
	survey = db.ReferenceProperty(Survey,required=True)
	username = db.StringProperty(required=True)
	choixProp = db.ReferenceProperty(Proposition, required=True) 
	
class Comment(db.Model):
	username = db.StringProperty(required=True)
	posted = db.DateTimeProperty(auto_now_add=True)
	message = db.TextProperty(required=True)
	trip_id = db.IntegerProperty(required=True)


	




