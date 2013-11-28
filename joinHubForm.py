import handler
import security
			
class JoinHubHandler(handler.Handler):
	def write_form(self, hubID="", error_hubID=""):
		self.render("joinHubForm.html",
		hub_ID=hubID,
		error_hubID=error_hubID) 

	def get(self):
		self.write_form();
		
	def post(self):
		hub_ID = self.request.get('hubID')
		hubID = security.valid_hub_id(str(hub_ID))
		error_hubID=""
        
		if not hubID:
			error_hubID = "The hub ID is numerical."
			self.write_form(str(hub_ID), error_hubID)
		else:
			self.redirect("/"+str(hub_ID))
