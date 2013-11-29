import handler
import security
import database
import cache
			
class CommentFormHandler(handler.Handler):
	def write_form(self,trip_id,username="", message="", error_username=""):
		trip=cache.get_trip(trip_id)
		if trip:
			comments=cache.get_comments(trip_id)
			self.render("commentForm.html", trip=trip, comments=comments, username=username, message=message, error_username=error_username) 
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
			self.write_form(trip_id,user_name,message,"That's not a valid username.")
		else:
			trip=cache.get_trip(trip_id)
			e = database.Comment(parent=trip,username=user_name,trip_id=int(trip_id),message=message).put()
			cache.update_comments(trip_id)
			self.redirect("/"+trip_id)
