import models.helpers as h
from models.Handler import Handler
from models.User import User
from google.appengine.ext import ndb

class LoginPage(Handler):
    """
    Class for handling logins
    """
    def get(self):
        """
        Handles the GET request for the login page
        """
        self.render("login.html")

    def post(self):
        """
        Handles the POST request for the login page
        """
        username_error = ""
        password_error = ""

        username = self.request.get("username")
        password = self.request.get("password")

        if not h.valid_username(username):
            username_error = "Username is invalid"

        if not h.valid_password(password):
            password_error = "Password is not valid"

        if username_error == "" and password_error == "":
            user = User.query().filter(User.username == username).fetch(1)

            if not user:
                self.render("login.html", username_error="Login failed")
            else:
                user = user[0]
                password = h.encrypt_password(password)

                if password != user.password:
                    self.render(
                        "login.html",
                        username=username,
                        password_error="Username and password do not match")
                else:
                    pw_hash = h.make_pw_hash(username, password)
                    self.response.headers.add_header(
                        'Set-Cookie',
                        'user=%s|%s; Path=/' % (str(user.key.id()), pw_hash))
                    self.redirect("/")
        else:
            self.render(
                "login.html",
                username=username,
                username_error=username_error,
                password_error=password_error)
