import os
import webapp2
import jinja2
import models.helpers as h

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '../templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)

class Handler(webapp2.RequestHandler):
    """
    Provides convenience methods for rendering templates
    """
    def write(self, *a, **kw):
        """
        Simplifies the method call to write the response
        """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """
        Converts the jina template into a string
        """
        template = JINJA_ENV.get_template(template)
        return template.render(params)

    def render(self, template, **kw):
        """
        Writes the string template provided from the render_str method
        """
        self.write(self.render_str(template, **kw))

    def authenticate_user(self):
        '''
        Authenticates and returns the current user
        Returns None if the user cookie does not exist
        '''
        user_cookie = self.request.cookies.get('user')
        if not user_cookie:
            return None
        else:
            user_hash = h.get_user_from_cookie(user_cookie)
            if user_hash[0] and user_hash[1]:
                user = user_hash[0]
                pw_hash = user_hash[1]
                # cookie exists but password does not match
                # so we call log out to clear the cookie
                if not h.valid_pw(user.username, user.password, pw_hash):
                    self.redirect("/logout")

                return user
