import webapp2
        
import hub
import trip
import tripForm
import error
import joinHubForm
import places
		
app = webapp2.WSGIApplication([('/', hub.HubHandler),
								('/_create', tripForm.TripFormHandler),
								('/_join', joinHubForm.JoinHubHandler),
								('/_places', places.placesHandler),
								('/(\d+)', trip.TripHandler),
								('/.*', error.ErrorHandler)
								]
								, debug=True)