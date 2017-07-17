import os
import re
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
	return USER_RE.match(username)

def valid_password(password):
	return PASSWORD_RE.match(password)

def valid_verify(password, verify):
	return valid_password(password) and password == verify

def valid_email(email):
	return not email or EMAIL_RE.match(email)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		self.render("signup.html")

	def post(self):
		username_error = ""
		password_error = ""
		verify_error = ""
		email_error = ""
		
		username = self.request.get("username")
		email = self.request.get("email")
		password = self.request.get("password")
		verify = self.request.get("verify")

		if not valid_username(username):
			username_error = "Username is invalid"

		if not valid_password(password):
			password_error = "Password is not valid"

		if not valid_email(email):
			email_error = "Email is not valid"

		if not valid_verify(password, verify):
			verify_error = "Your passwords didn't match"

		if valid_email(email) and valid_username(username) and valid_verify(password, verify):
			self.redirect("/welcome?username=" + username)
		else:
			self.render(
				"signup.html", 
				username = username, 
				username_error = username_error, 
				password_error = password_error, 
				email_error = email_error,
				verify_error = verify_error)

class WelcomePage(Handler):
	def get(self):
		username = self.request.get("username")
		self.render("welcome.html", username=username)

app = webapp2.WSGIApplication([
	('/', MainPage), ('/welcome', WelcomePage)], debug=True)