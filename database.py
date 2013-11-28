import handler

from google.appengine.ext import db

	
class Discussion(db.Model):
	id = db.StringProperty(required=True) //hash de title email salt
	title = db.StringProperty(required=True)
	comments = db.ListProperty(Comment, required=True)
	sondages = db.ListProperty(Sondage, required=True)

class Comment(db.Model):
	username = db.StringProperty(required=True)
	posted = db.DateTimeProperty(auto_now_add=True)
	message = db.TextProperty(required=True)
	
	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return handler.render_str("post.html", p = self)
	
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
	answers = db.ListProperty(Proposition,required=True)
	result = db.ReferenceProperty(Reponse,required=False)
	