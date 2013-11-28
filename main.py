import webapp2
        
import hub 		

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
		
app = webapp2.WSGIApplication([('/', hub.HubHandler),
								(PAGE_RE, hub.HubHandler)
								]
								, debug=True)