from models.Handler import Handler

class LogoutPage(Handler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % "")
		self.redirect("/login")
