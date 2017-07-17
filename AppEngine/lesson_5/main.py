import os

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Art(db.Model):
	title = db.StringProperty(required = True)
	ascii = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
	def render_front(self, title="", ascii="", error=""):
		arts = db.GqlQuery("select * from Art order by created desc")
		
		self.render("main.html", title=title, ascii=ascii, error=error, arts=arts)

	def get(self):
		self.render_front()

	def post(self):
		ascii = self.request.get("ascii")
		title = self.request.get("title")

		if not ascii or not title:
			self.render_front(title, ascii, "We need both a title and some art")
		else:
			art = Art(title=title, ascii=ascii)
			art.put()
			
			self.redirect("/")

app = webapp2.WSGIApplication([
	('/', MainPage)], debug=True)