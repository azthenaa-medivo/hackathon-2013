import handler
import security
import database
import cache
from operator import attrgetter
from google.appengine.ext import db
			
class SurveyListHandler(handler.Handler):
	def write_list(self,trip_id,username="",error_username=""):
		trip=cache.get_trip(trip_id)
		if trip:
			surveys=cache.get_surveys(trip_id)
			surveys_real=db.GqlQuery("SELECT * FROM Survey WHERE trip_id = :1 ORDER BY posted DESC",int(trip_id)).fetch(None)
			for survey in surveys_real:
				propositions=cache.get_propositions(trip_id,survey.key().id())
				propositions_real=db.GqlQuery("SELECT * FROM Proposition WHERE survey_id = :1 ORDER BY posted DESC",int(trip_id)).fetch(None)
			#surveyMax = []
			#for survey in surveys:
			#	bestProposition=max(survey.propositions,key=attrgetter('votes'))
			#	if bestProposition :
			#		surveyMax.append(bestProposition)
			#	else :
			#		surveyMax.append(survey.propositions[0])
			#surveysPlusMax=zip(surveys,surveyMax)
			self.render("surveys.html", trip=trip, surveys=surveys, username=username, error_username=error_username)
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
			#surveys=self.request.get('surveys')
			surveys=cache.get_surveys(trip_id)
			for survey in surveys:
				propButton = self.request.get('vote'+str(survey.key().id()))
				if propButton:
					voteKey = self.request.get('group'+str(survey.key().id()))
					propositionVotee = cache.get_proposition(trip_id, voteKey)
					previousReponse = cache.get_reponse(trip_id, voteKey)
					
					if(previousReponse.count()==0):
						propositionVotee.votes+=1
						propositionVotee.put()
						cache.update_proposition(trip_id, voteKey)
						
						rep = database.Reponse(survey=survey,username=user_name,choixProp=propositionVotee)				
						rep.put()
						cache.update_reponse(trip_id, voteKey)
					elif(previousReponse.count()==1):
						previousReponse[0].choixProp=propositionVotee
						previousReponse[0].put()
						cache.update_reponse(trip_id, voteKey)
					break

			self.write_list(trip_id);
