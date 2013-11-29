import database
from google.appengine.api import memcache
from google.appengine.ext import db
	
def get_trip(trip_id):
	key = str(trip_id)
	trip = memcache.get(key)
	if trip is None or not trip:
		trip = database.Discussion.get_by_id(int(trip_id))
		if trip:
			memcache.set(key,trip)
	return trip
	
def get_survey(trip_id,survey_id):
	keySurvey=trip_id+"surveys"
	surveys=memcache.get(keySurvey)
	if surveys is None or not surveys:
		surveys=get_surveys(trip_id)
		
	bonSurvey=None
	for survey in surveys:
		if survey.key().id()==str(survey_id):
			bonSurvey=survey
	return bonSurvey

def get_comments(trip_id):
	key=trip_id+"comments"
	comments = memcache.get(key)
	if comments is None or not comments:
		trip=get_trip(trip_id)
		comments=db.GqlQuery("SELECT * FROM Comment WHERE ANCESTOR IS :1 ORDER BY posted DESC",trip.key()).fetch(None)
		comments=list(comments)
		memcache.set(key,comments)
	return comments
	
def update_comments(trip_id):
	key=trip_id+"comments"
	trip=get_trip(trip_id)
	comments=db.GqlQuery("SELECT * FROM Comment WHERE ANCESTOR IS :1 ORDER BY posted DESC",trip.key()).fetch(None)
	comments=list(comments)
	memcache.set(key,comments)
	
def get_surveys(trip_id):
	key=trip_id+"surveys"
	surveys=memcache.get(key)
	if surveys is None or not surveys:
		trip=get_trip(trip_id)
		surveys=db.GqlQuery("SELECT * FROM Survey WHERE ANCESTOR IS :1 ORDER BY posted DESC",trip.key()).fetch(None)
		surveys=list(surveys)
		memcache.set(key,surveys)
	return surveys
	
def update_surveys(trip_id):
	key=str(trip_id)+"surveys"
	trip=get_trip(trip_id)
	surveys=db.GqlQuery("SELECT * FROM Survey WHERE ANCESTOR IS :1 ORDER BY posted DESC",trip.key()).fetch(None)
	surveys=list(surveys)
	memcache.set(key,surveys)

def get_propositions(trip_id, survey_id):
	key=str(survey_id)+"propositions"
	propositions=memcache.get(key)
	if propositions is None or not propositions:
		survey=get_survey(trip_id,survey_id)
		propositions=db.GqlQuery("SELECT * FROM Proposition WHERE ANCESTOR IS :1 ORDER BY numero ASC",survey.key()).fetch(None)
		propositions=list(propositions)
		memcache.set(key,propositions)
	return propositions
	
def update_propositions(trip_id, survey_id):	
	survey = get_survey(trip_id,survey_id)		
	propositions=db.GqlQuery("SELECT * FROM Proposition WHERE ANCESTOR IS :1 ORDER BY numero ASC",survey.key()).fetch(None)
	propositions=list(propositions)
	
	key=str(survey_id)+"propositions"
	memcache.set(key,propositions)
	
def get_reponse(trip_id, voteKey):
	key=trip_id+voteKey+"reponse"
	reponse=memcache.get(key)
	if reponse is None or not reponse:
		p=db.get(voteKey)
		reponse=db.GqlQuery("SELECT * FROM Reponse WHERE username = "+p.username,trip_id).fetch(None)
		memcache.set(key,reponse)
	return reponse
	
def update_reponse(trip_id,rep):
	key=str(trip_id)+"rep"+str(rep.key().id())
	memcache.set(key,rep)
	
