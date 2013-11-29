import handler
import cache
import security
import database

from google.appengine.ext import db

class TripHandler(handler.Handler):

	def render_trip(self, trip_id):
		trip = cache.get_trip(trip_id)
		if trip is not None:
			comments=cache.get_comments(trip_id)
			comments_real=db.GqlQuery("SELECT * FROM Comment WHERE trip_id = :1 ORDER BY posted DESC",int(trip_id)).fetch(None)
			self.render("trip.html",trip=trip,comments=comments,comments_real=comments_real)
		else:
			self.redirect("/error")

	def get(self,trip_id):
		self.render_trip(trip_id);