import handler

from google.appengine.ext import db

class Comment(db.Model):
	username = db.StringProperty(required=True)
	posted = db.DateTimeProperty(auto_now_add=True)
	message = db.TextProperty(required=True)
	
	def __cmp__(self, other):
		if self.posted > other.posted:
			return 1
		elif self.posted < other.posted:
			return -1
		else:
			return 0

class Proposition(db.Model):
	numero = db.IntegerProperty(required = True)
	text = db.TextProperty(required=True)
	
class Reponse(db.Model):
	username = db.StringProperty(required=True)
	choixProp = db.ReferenceProperty(Proposition, required=True) 

class Sondage(db.Model):
	username = db.StringProperty(required=True)
	posted = db.DateTimeProperty(auto_now_add=True)
	question = db.TextProperty(required=True)
	answers = db.ListProperty(db.Key,required=True)
	result = db.ReferenceProperty(Reponse,required=False)

class Discussion(db.Model):
	title = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	comments = db.ListProperty(db.Key,required=True)
	sondages = db.ListProperty(db.Key,required=True)