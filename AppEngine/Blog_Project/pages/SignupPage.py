import models.helpers as h
from models.Handler import Handler
from models.User import User

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

		if not h.valid_username(username):
			username_error = "Username is invalid"

		if not h.valid_password(password):
			password_error = "Password is not valid"

		if not h.valid_email(email):
			email_error = "Email is not valid"

		if not h.valid_verify(password, verify):
			verify_error = "Your passwords didn't match"

		if h.valid_email(email) and h.valid_username(username) and h.valid_verify(password, verify):
			user = User.query().filter(User.username_lower == username.lower()).fetch(1)
			if user:
				self.render(
					"signup.html",
					username = username,
					username_error = "Username not available",
					password_error = password_error,
					email_error = email_error,
					verify_error = verify_error)
			else:
				password = h.encrypt_password(password)
				user = User(username=username, username_lower=username.lower(), password=password)
				user.put()

				id = user.key.id()
				hash = h.make_pw_hash(username, password)
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