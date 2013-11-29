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