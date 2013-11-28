import webapp2
        
import hub
import tripForm

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
		
app = webapp2.WSGIApplication([('/', hub.HubHandler),
								('/_create', tripForm.TripFormHandler),
								(PAGE_RE, hub.HubHandler)
								]
								, debug=True)