import handler
import cache
import security
import database

class TripHandler(handler.Handler):

	def render_trip(self, trip=None, comments=[],error_username=""):
		if trip is not None:
			self.render("trip.html",trip=trip,comments=comments,error_username=error_username)
		else:
			self.response.out.write("This is not the trip you are looking for !")

	def get(self,trip_id):
		trip = cache.get_trip(trip_id)
		comments=[]
		self.render_trip(trip,comments,"");
		
	def post(self,trip_id):
		form_type = self.request.get('formType')
		trip = cache.get_trip(trip_id)
		comments=[]
		if form_type == "commentForm":
			self.add_comment(trip,comments)
			
	def add_comment(self,trip,comments=[]):
		username = self.request.get('username')
		message = self.request.get('message')
		valid_username=security.valid_user_name(username)
		if not valid_username:
			self.render_trip(trip,comments,"That's not a valid username.");
		else:
			e = database.Comment(username=username,message=message)
			e.put()
			trip.comments.append(e.key())
			comments.append(e)
			self.render_trip(trip,comments,"")