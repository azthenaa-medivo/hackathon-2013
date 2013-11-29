import handler
import cache
import security
import database

from google.appengine.ext import db

class TripHandler(handler.Handler):

	def render_trip(self, trip_id,comment_username="",comment_message="",error_username=""):
		trip = cache.get_trip(trip_id)
		if trip is not None:
			comments=cache.get_comments(trip_id)
			self.render("trip.html",trip=trip,comments=comments, comment_username=comment_username, comment_message=comment_message, error_username=error_username)
		else:
			self.redirect("/error")

	def get(self,trip_id):
		self.render_trip(trip_id);
		
	def post(self,trip_id):
		user_name = self.request.get('username')
		message = self.request.get('message')

		username = security.valid_user_name(user_name)

		error_username=""
        
		if not username :
			self.write_form(trip_id,user_name,message,"That's not a valid username.")
		else:
			trip=cache.get_trip(trip_id)
			e = database.Comment(parent=trip,username=user_name,trip_id=int(trip_id),message=message).put()
			cache.update_comments(trip_id)
			self.redirect("/"+trip_id)