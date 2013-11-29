import handler
import security
import database
import cache
from operator import attrgetter
from google.appengine.ext import db

import logging
			
class SurveyListHandler(handler.Handler):
	def write_list(self,trip_id,username="",error_username=""):
		trip=cache.get_trip(trip_id)
		if trip:
			surveys=cache.get_surveys(trip_id)
			
			surveyProp=[]
			for survey in surveys:
				propositions=cache.get_propositions(trip_id,survey.key().id())
				surveyProp.append(propositions)
			
			
			#surveyMax = []
			#for survey in surveys:
			#	bestProposition=max(survey.propositions,key=attrgetter('votes'))
			#	if bestProposition :
			#		surveyMax.append(bestProposition)
			#	else :
			#		surveyMax.append(survey.propositions[0])
			#surveysPlusMax=zip(surveys,surveyMax)
			
			
			surveysPlusProp = zip(surveys,surveyProp)
			self.render("surveys.html", trip=trip, surveysPlusProp=surveysPlusProp, username=username, error_username=error_username)
		else:
			self.redirect("/error")

	def get(self,trip_id):
		self.write_list(trip_id);
		
	def post(self,trip_id):
		user_name = self.request.get('username')
		username = security.valid_user_name(user_name)

		error_username=""
        
		if not username :
			self.write_form(trip_id,user_name,message,"That's not a valid username.")
		else:
			surveys=cache.get_surveys(trip_id)
			for survey in surveys:
				surveyID=survey.key().id()
				propButton = self.request.get('vote'+str(surveyID))
				if propButton:
					choixVote = self.request.get('group'+str(surveyID))
					propositionVotee = cache.get_proposition(trip_id,surveyID,choixVote)
					previousReponse = cache.get_reponse(trip_id,surveyID,username)
					
					if not previousReponse:
						propositionVotee.votes+=1
						propositionVotee.put()
						cache.update_propositions(trip_id, surveyID)
						
						rep = database.Reponse(parent=survey,username=user_name,choixProp=propositionVotee)				
						rep.put()
						cache.update_reponses(trip_id, surveyID)
					else:
						previousReponse.choixProp.votes-=1
						previousReponse.choixProp.put()
						cache.update_propositions(trip_id, surveyID)
						
						previousReponse.choixProp=propositionVotee
						previousReponse.put()
						cache.update_reponses(trip_id, surveyID)
					break
			
			self.write_list(trip_id);