import handler

class HubHandler(handler.Handler):
	def render_hub(self):
		self.render("hub.html")
		
	def get(self):
		self.render_hub();