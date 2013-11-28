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
			get_comments(trip_id)
	return trip

def get_comments(trip_id):
	key=trip_id+"comments"
	comments=memcache.get(key)
	if comments is None or not comments:
		trip=get_trip(trip_id)
		comments=database.Comment.get(trip.comments)
		if comments:
			comments=sorted(comments)
			memcache.set(key,comments)
	return comments