import webapp2
        
import hub
import trip
import tripForm
		
app = webapp2.WSGIApplication([('/', hub.HubHandler),
								('/_create', tripForm.TripFormHandler),
								('/_join', tripForm.JoinHubHandler),
								('/(\d+)', trip.TripHandler)
								]
								, debug=True)