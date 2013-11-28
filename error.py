import handler

class ErrorHandler(handler.Handler):
	def write_form(self):
		self.render("error.html")

	def get(self):
		self.write_form();