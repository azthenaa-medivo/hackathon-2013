import re
import cgi
import string

def escape_html(s):
	return cgi.escape(s, quote = True)
	
class ErrorHandler(handler.Handler):
	def write_form(self):
		self.render("error.html")

	def get(self):
		self.write_form();