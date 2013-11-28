import webapp2
        
import hub
import trip
import tripForm
import error
import joinHubForm
import commentForm
import shareTrip
		
app = webapp2.WSGIApplication([('/', hub.HubHandler),
								('/_create', tripForm.TripFormHandler),
								('/_join', joinHubForm.JoinHubHandler),
								('/(\d+)', trip.TripHandler),
								('/(\d+)/comment', commentForm.CommentFormHandler),
								('/(\d+)/share', shareTrip.ShareTripHandler),
								('/.*', error.ErrorHandler)
								]
								, debug=True)