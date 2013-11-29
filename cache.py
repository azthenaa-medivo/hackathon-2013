import database

from google.appengine.api import memcache
from google.appengine.ext import db
	
def get_trip(trip_id):
	key = trip_id
	trip = memcache.get(key)
	if trip is None or not trip:
		trip = database.Discussion.get_by_id(int(trip_id))
		if trip:
			memcache.set(key,trip)
	return trip

def get_comments(trip_id):
	key=trip_id+"comments"
	comments=memcache.get(key)
	if comments is None or not comments:
		comments=db.GqlQuery("SELECT * FROM Comment WHERE trip_id = :1 ORDER BY posted DESC",trip_id).fetch(None)
		comments=list(comments)
		memcache.set(key,comments)
	return comments
	
def update_comments(trip_id):
	key=str(trip_id)+"comments"
	comments=db.GqlQuery("SELECT * FROM Comment WHERE trip_id = :1 ORDER BY posted DESC",trip_id).fetch(None)
	comments=list(comments)
	memcache.set(key,comments)
	
def get_surveys(trip_id):
	key=trip_id+"surveys"
	surveys=memcache.get(key)
	if surveys is None or not surveys:
		surveys=db.GqlQuery("SELECT * FROM Survey WHERE trip_id = :1 ORDER BY posted DESC",trip_id).fetch(None)
		surveys=list(surveys)
		memcache.set(key,surveys)
	return surveys
	
def update_surveys(trip_id):
	key=str(trip_id)+"surveys"
	surveys=db.GqlQuery("SELECT * FROM Survey WHERE trip_id = :1 ORDER BY posted DESC",trip_id).fetch(None)
	surveys=list(surveys)
	memcache.set(key,surveys)

def get_proposition(trip_id,voteKey):
	key=trip_id+"prop"+str(voteKey)
	proposition=memcache.get(key)
	if proposition is None or not proposition:
		proposition = db.get(voteKey)
		proposition=list(proposition)
		memcache.set(key,proposition)
	return proposition
	
def update_proposition(trip_id,prop):
	key=str(trip_id)+"prop"+str(prop.key().id())
	memcache.set(key,prop)
	
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
	
