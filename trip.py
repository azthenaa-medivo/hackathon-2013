import handler
import cache

class TripHandler(handler.Handler):
	def render_trip(self, trip=None):
		if trip is not None:
			self.render("trip.html",trip=trip)
		else:
			self.response.out.write("This is not the trip you are looking for !")

	def get(self,trip_id):
		trip = cache.get_trip(trip_id)
		self.render_trip(trip);