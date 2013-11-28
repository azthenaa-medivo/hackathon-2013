import database

from google.appengine.api import memcache
from google.appengine.ext import db
	
def get_trip(trip_id):
	key = trip_id
	trip = memcache.get(trip_id)
	if trip is None or not trip:
		trip = database.Discussion.get_by_id(int(trip_id))
		if trip:
			for comment in trip.comments:
				comment = trip.comment.replace('\n', '<br>')
			memcache.set(key,trip)
	return trip


