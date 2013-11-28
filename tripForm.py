from google.appengine.api import mail
from google.appengine.ext import db

import database
import handler
import security
import emailUtility

class TripFormHandler(handler.Handler):

	def write_form(self, user_name="", trip_name="", error_username="", error_email="", error_tripname=""):
		self.render("tripForm.html",
		user_name=user_name,
		trip_name=trip_name,
		error_username=error_username,
		error_email=error_email,
		error_tripname=error_tripname) 

	def get(self):
		self.write_form();
		
	def post(self):
		user_name = self.request.get('username')
		trip_name = self.request.get('tripname')
		email = self.request.get('email')

		username = security.valid_user_name(user_name) 
		tripname = security.valid_trip_name(trip_name)

		error_username=""
		error_tripname=""
		error_email=""
        
		if not username:
			error_username = "That's not a valid username."
		if not tripname :
			error_tripname = "That's not a valid trip name."
		if not mail.is_email_valid(email):
			error_email = "That's not a valid email."
			
		if error_username or error_email or error_tripname:
			self.write_form( security.escape_html(user_name), security.escape_html(trip_name), error_username, error_email, error_tripname)
		else:
			e = database.Discussion(title=trip_name)
			e.put()
			trip_id = str(e.key().id())
			emailUtility.send_email(user_name,trip_name,email,trip_id)
			self.redirect("/"+trip_id)