import handler

from google.appengine.ext import db

class Post(db.Model):
	subject=db.StringProperty(required=True)
	content=db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	
	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return handler.render_str("post.html", p = self)

class User(db.Model):
	username = db.StringProperty(required=True)
	hash = db.StringProperty(required=True)
	email = db.StringProperty(required = False )

class WikiPage(db.Model):
	version = db.IntegerProperty(required = True )
	content = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	pageName = db.StringProperty(required=True)
	author = db.StringProperty(required = True)
