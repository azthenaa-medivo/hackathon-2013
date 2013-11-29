import database
import logging
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
		if str(survey.key().id())==str(survey_id):
			bonSurvey=survey
			break
		
	return bonSurvey
	
def get_proposition(trip_id,survey_id,proposition_id):
	survey=get_survey(trip_id,survey_id)
	toutesPropos=get_propositions(trip_id,survey.key().id())	
	bonneProp=None
	for prop in toutesPropos:
		if str(prop.key().id()) == str(proposition_id):
			bonneProp=prop
			break
		
	return bonneProp
	
def get_reponse(trip_id,survey_id,username):
	survey=get_survey(trip_id,survey_id)
	toutesReponses=get_reponses(trip_id,survey.key().id())	
	bonneRep=None
	for rep in toutesReponses:
		if rep.username == username:
			bonneRep=rep
			break
		
	return bonneRep

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
	key=str(trip_id)+"surveys"
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
	
def get_reponses(trip_id, survey_id):
	key=str(survey_id)+"reponses"
	reponses=memcache.get(key)
	if reponses is None or not reponses:
		survey=get_survey(trip_id,survey_id)
		reponses=db.GqlQuery("SELECT * FROM Reponse WHERE ANCESTOR IS :1 ORDER BY username ASC",survey.key()).fetch(None)
		reponses=list(reponses)
		memcache.set(key,reponses)
	return reponses
	
def update_reponses(trip_id, survey_id):
	survey = get_survey(trip_id,survey_id)		
	reponses=db.GqlQuery("SELECT * FROM Reponse WHERE ANCESTOR IS :1 ORDER BY username ASC",survey.key()).fetch(None)
	reponses=list(reponses)	
	key=str(survey_id)+"reponses"
	memcache.set(key,reponses)
	
