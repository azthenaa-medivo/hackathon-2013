import webapp2
        
import hub
import trip
import tripForm
import error
import joinHubForm
		
app = webapp2.WSGIApplication([('/', hub.HubHandler),
								('/_create', tripForm.TripFormHandler),
								('/_join', joinHubForm.JoinHubHandler),
								('/(\d+)', trip.TripHandler),
								('/.*', error.ErrorHandler)
								]
								, debug=True)