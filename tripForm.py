from google.appengine.ext import db

import database
import handler
import security

class TripFormHandler(handler.Handler):
	def write_form(self, user_name="", trip_name="", error_username="", error_tripname=""):
		self.render("tripForm.html",
		user_name=user_name,
		trip_name=trip_name,
		error_username=error_username,
		error_tripname=error_tripname) 

	def get(self):
		self.write_form();
		
	def post(self):
		user_name = self.request.get('username')
		trip_name = self.request.get('tripname')

		username = security.valid_user_name(user_name) 
		tripname = security.valid_trip_name(trip_name)

		error_username=""
		error_tripname=""
        
		if not username :
			error_username = "That's not a valid username."
		if not tripname :
			error_tripname = "That wasn't a valid trip name."

		if not (username and tripname):
			self.write_form( security.escape_html(user_name), security.escape_html(trip_name), error_username, error_tripname)
		else:
			e = database.Discussion(title=trip_name,comments=[],sondages=[])
			e.put()
			self.redirect("/"+str(e.key().id()))