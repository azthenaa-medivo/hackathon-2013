import handler
import cache
import security
import database

class TripHandler(handler.Handler):

	def render_trip(self, trip_id):
		trip = cache.get_trip(trip_id)
		if trip is not None:
			comments=cache.get_comments(trip_id)
			self.render("trip.html",trip=trip,comments=comments)
		else:
			self.redirect("/error")

	def get(self,trip_id):
		self.render_trip(trip_id);