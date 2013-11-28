import webapp2
        
import hub
import trip	

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
		
app = webapp2.WSGIApplication([('/', hub.HubHandler),
								('/_create', trip.TripHandler),
								(PAGE_RE, hub.HubHandler)
								]
								, debug=True)