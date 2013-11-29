import handler
import security
import database
import cache
			
class SurveyFormHandler(handler.Handler):
	def write_form(self,trip_id,username="", question="", listProp=[""], error_username=""):
		trip=cache.get_trip(trip_id)
		self.render("surveyForm.html", trip=trip, listProp=listProp, username=username, question=question, error_username=error_username) 

	def get(self,trip_id):
		self.write_form(trip_id);
		
	def post(self,trip_id):
		user_name = self.request.get('username')
		question = self.request.get('question')
		
		listProp=self.request.get_all('propText')			
		propButton = self.request.get('propButton')

		if propButton:
			listProp.append("")
			self.write_form(trip_id, user_name, question, listProp, "")
			
		else:		
			username = security.valid_user_name(user_name)
			error_username=""
			
			if not username :
				self.write_form(trip_id,user_name,question,listProp,"That's not a valid username.")
			else:
				
				trip=cache.get_trip(trip_id)
				e = database.Survey(parent=trip, username=user_name,question=question)
				e.put()
				
				for num, prop in enumerate(listProp):
					tempProp = database.Proposition(parent=e, numero=num+1, text=prop, votes=0)
					tempProp.put()
				
				cache.update_surveys(int(trip_id))
				#cache.update_propositions(trip_id,e.key().id())
				self.redirect("/"+trip_id+"/surveys")
