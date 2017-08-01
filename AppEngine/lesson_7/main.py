import os
import random
import re
import webapp2
import jinja2
import hashlib
import hmac
import string

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

SECRET = 'imsosecret'
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
COOKIE_RE = re.compile(r'.+=;\s*Path=/')

def valid_cookie(cookie):
    return cookie and COOKIE_RE.match(cookie)

def valid_username(username):
	return USER_RE.match(username)

def valid_password(password):
	return PASSWORD_RE.match(password)

def valid_verify(password, verify):
	return valid_password(password) and password == verify

def valid_email(email):
	return not email or EMAIL_RE.match(email)

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def valid_pw(name, pw, h):
	try:
		salt = h.split('|')[1]
		hash = hashlib.sha256(name + pw + salt).hexdigest()
		return h == ('%s|%s' % (hash, salt))
	except: 
		return None

def make_pw_hash(name, pw):
	salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s|%s' % (h, salt)

class User(db.Model):
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

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
		user_cookie = self.request.cookies.get('user')

		if not user_cookie:
			self.redirect("/login")
		else:
			strings = user_cookie.split('|')
			id = int(strings[0])
			hash = '%s|%s' % (strings[1], strings[2])

			user = User.get_by_id(id)
			
			if not user:
				self.redirect("/signup")
			elif not valid_pw(user.username, user.password, hash):
				self.redirect("/signup")
			else:
				self.render("main.html", username=user.username)	

class SignupPage(Handler):
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
			user = User.gql("WHERE username = :1", username)
			if user:
				self.render(
					"signup.html", 
					username = username, 
					username_error = "Username not available", 
					password_error = password_error, 
					email_error = email_error,
					verify_error = verify_error)

			user = User(username=username, password=password)
			user.put()

			id = user.key().id()
			hash = make_pw_hash(username, password)
			self.response.headers.add_header('Set-Cookie', 'user=%s|%s; Path=/' % (id, hash))
			self.redirect("/")
			
		else:
			self.render(
				"signup.html", 
				username = username, 
				username_error = username_error, 
				password_error = password_error, 
				email_error = email_error,
				verify_error = verify_error)

class LoginPage(Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		username_error = ""
		password_error = ""
		
		username = self.request.get("username")
		password = self.request.get("password")

		if not valid_username(username):
			username_error = "Username is invalid"

		if not valid_password(password):
			password_error = "Password is not valid"

		if username_error == "" and password_error == "":
			q = db.GqlQuery("SELECT * FROM User WHERE username = :username", username=username)
			user = q.get()
			hash = make_pw_hash(username, password)

			if password != user.password:
				self.render(
					"login.html", 
					username = username, 
					password_error = "Username and password do not match")

			self.response.headers.add_header('Set-Cookie', 'user=%s|%s; Path=/' % (str(user.key().id()), hash))
			self.redirect("/")
			
		else:
			self.render(
				"login.html", 
				username = username, 
				username_error = username_error, 
				password_error = password_error)

class LogoutPage(Handler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % "")
		self.redirect("/signup")

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/signup', SignupPage),
	("/login", LoginPage),
	("/logout", LogoutPage)], debug=True)