import handler
import security
import database
import cache
from operator import attrgetter
from google.appengine.ext import db

import logging
			
class SurveyListHandler(handler.Handler):
	def write_form(self,trip_id,user_nameCreate="",user_nameAnswer="",question="",listProp=[""],error_username=""):
		trip=cache.get_trip(trip_id)
		if trip:
			surveys=cache.get_surveys(trip_id)
			
			surveyProp=[]
			for survey in surveys:
				propositions=cache.get_propositions(trip_id,survey.key().id())
				surveyProp.append(propositions)
			
			surveysPlusProp = zip(surveys,surveyProp)
			self.render("surveys.html", trip=trip, surveysPlusProp=surveysPlusProp, usernameCreate=user_nameCreate,usernameAnswer=user_nameAnswer, error_username=error_username, question=question, listProp=listProp)
		else:
			self.redirect("/error")

	def get(self,trip_id):
		self.write_form(trip_id);
		
	def post(self,trip_id):
		createButton = self.request.get('createButton')		
		propButton = self.request.get('propButton')
		
		question = self.request.get('question')
		user_nameCreate = self.request.get('usernameCreate')
		listProp=self.request.get_all('propText')
		user_nameAnswer = self.request.get('usernameAnswer')
		
		if createButton:		
			
			if not security.valid_user_name(user_nameCreate) :
				self.write_form(trip_id,user_nameCreate,user_nameAnswer,question,listProp,"That's not a valid username.")
			else:
				
				trip=cache.get_trip(trip_id)
				e = database.Survey(parent=trip, username=user_nameCreate,question=question)
				e.put()
				
				for num, prop in enumerate(listProp):
					tempProp = database.Proposition(parent=e, numero=num+1, text=prop, votes=0)
					tempProp.put()
				
				cache.update_surveys(int(trip_id))
				cache.update_propositions(trip_id,e.key().id())
				self.redirect("/"+trip_id+"/surveys")
	
		elif propButton :
			listProp.append("")
			self.write_form(trip_id,user_nameCreate,user_nameAnswer,question,listProp,"")
		
		else :		
		
			if not security.valid_user_name(user_nameAnswer) :
				self.write_form(trip_id,user_nameCreate,user_nameAnswer,question,listProp,"That's not a valid username.")
			else:
				surveys=cache.get_surveys(trip_id)
				for survey in surveys:
					surveyID=survey.key().id()
					choixButton = self.request.get('vote'+str(surveyID))
					if choixButton:
						choixVote = self.request.get('group'+str(surveyID))
						propositionVotee = cache.get_proposition(trip_id,surveyID,choixVote)
						previousReponse = cache.get_reponse(trip_id,surveyID,user_nameAnswer)
						
						if previousReponse:
							previousReponse.choixProp.votes-=1
							(previousReponse.choixProp).put()
							propositionVotee.put()
							cache.update_propositions(trip_id, surveyID)
							
							previousReponse.choixProp=propositionVotee
							previousReponse.put()
							cache.update_reponses(trip_id, surveyID)
						else:
							propositionVotee.votes+=1
							propositionVotee.put()
							cache.update_propositions(trip_id, surveyID)
							
							rep = database.Reponse(parent=survey,username=user_nameAnswer,choixProp=propositionVotee)				
							rep.put()
							cache.update_reponses(trip_id, surveyID)
							
						break
				
				self.redirect("/"+trip_id+"/surveys")