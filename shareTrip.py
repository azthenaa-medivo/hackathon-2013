from google.appengine.api import mail

import handler
import emailUtility
import cache

# Adapted from https://developers.google.com/appengine/docs/python/mail/sendingmail?hl=fr

class ShareTripHandler(handler.Handler):
	def write_form(self,trip,email="",error_email=""):
		self.render("shareTrip.html",trip=trip,email=email,error_email=error_email)

	def get(self,trip_id):
		self.write_form(cache.get_trip(trip_id));

	def post(self,trip_id):
		email = self.request.get("email")
		message = self.request.get("message")		
		if not mail.is_email_valid(email):
			self.write_form(cache.get_trip(trip_id).title,email,"That's not a valid email.");
		else:
			emailUtility.share_trip(email,message)
			self.redirect("/"+trip_id)
