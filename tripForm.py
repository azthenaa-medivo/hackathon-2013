import re
import cgi
import random
import string
import hashlib

from google.appengine.ext import db

import database
import handler

USER_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
TRIP_NAME_REGEX = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_\s]{3,200}$")

def valid_user_name(user_name):
	return USER_NAME_REGEX.match(user_name)

def valid_trip_name(trip_name):
	return TRIP_NAME_REGEX.match(trip_name)
	
def escape_html(s):
	return cgi.escape(s, quote = True)

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

		username = valid_user_name(user_name) 
		tripname = valid_trip_name(trip_name)

		error_username=""
		error_tripname=""
        
		if not username :
			error_username = "That's not a valid username."
		if not tripname :
			error_tripname = "That wasn't a valid trip name."

		if not (username and tripname):
			self.write_form( escape_html(user_name), escape_html(trip_name), error_username, error_tripname)
		else:
			e = database.Discussion(title=trip_name,comments=[],sondages=[])
			e.put()
			self.redirect("/"+str(e.key().id()))