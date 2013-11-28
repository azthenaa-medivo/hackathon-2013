import webapp2
        
import hub
import trip
import tripForm
		
app = webapp2.WSGIApplication([('/', hub.HubHandler),
								('/_create', tripForm.TripFormHandler),
								('/(\d+)', trip.TripHandler)
								]
								, debug=True)