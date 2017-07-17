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

class Post(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
	def get(self):
		posts = db.GqlQuery("select * from Post order by created desc")		
		self.render("main.html", posts=posts)

class NewPostPage(Handler):
	def render_front(self, title="", content="", error=""):
		self.render("new_post.html", title=title, content=content, error=error)

	def get(self):
		self.render_front()

	def post(self):
		content = self.request.get("content")
		title = self.request.get("subject")

		if not content or not title:
			self.render_front(title, content, "We need both a title and content")
		else:
			post = Post(title=title, content=content)
			post.put()
			
			self.redirect("/post/" + str(post.key().id()))


class PostPage(Handler):
	def get(self, post_id):
		if not post_id:
			self.render("post.html", error="No post id provided")
		
		post = Post.get_by_id(long(post_id))

		if not post:
			self.render("post.html", error="A post could not be found that matches the provided id")
		else:
			self.render("post.html", post=post)

app = webapp2.WSGIApplication([
	('/', MainPage), 
	("/newpost", NewPostPage),
	("/post/(\d+)", PostPage)], debug=True)