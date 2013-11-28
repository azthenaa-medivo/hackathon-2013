import handler
import security
import database
import cache
			
class CommentFormHandler(handler.Handler):
	def write_form(self,trip_id,username="", message="", error_username=""):
		trip=cache.get_trip(trip_id)
		if trip:
			self.render("commentForm.html", trip=trip, username=username, message=message, error_username=error_username) 
		else:
			self.redirect("/error")

	def get(self,trip_id):
		self.write_form(trip_id);
		
	def post(self,trip_id):
		user_name = self.request.get('username')
		message = self.request.get('message')

		username = security.valid_user_name(user_name)

		error_username=""
        
		if not username :
			self.write_form(trip_id,username,message,"That's not a valid username.")
		else:
			e = database.Comment(username=user_name,trip_id=int(trip_id),message=message)
			e.put()
			self.redirect("/"+trip_id)
