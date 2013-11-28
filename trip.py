import re
import cgi

from google.appengine.ext import db

import handler

NAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

def valid_name(name):
	return NAME_REGEX.match(name)

def escape_html(s):
	return cgi.escape(s, quote = True)

class TripHandler(handler.Handler):
	def write_form(self, user_name="", trip_name="", error_username="", error_tripname=""):
		self.render("trip.html",
		user_name=user_name,
		trip_name=trip_name,
		error_username=error_username,
		error_tripname=error_tripname) 

	def render_trip(self):
		self.render("trip.html")

	def get(self):
		self.render_trip();
		
	def post(self):
		user_name = self.request.get('username')
		trip_name = self.request.get('tripname')

		username = valid_name(user_name) 
		tripname = valid_name(trip_name)

		error_username=""
		error_tripname=""
        
		if not username :
			error_username = "That's not a valid username."
		if not tripname :
			error_tripname = "That wasn't a valid trip name."

		if not (username and tripname):
			self.write_form( escape_html(user_name), escape_html(trip_name), error_username, error_tripname)
		else:
			self.redirect("/")