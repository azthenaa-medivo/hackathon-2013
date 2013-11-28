import handler

class HubHandler(handler.Handler):
	def render_hub(self):
		self.render("hub.html")
		
	def get(self,id=None):
		self.render_hub();