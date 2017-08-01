from google.appengine.ext import ndb

class Post(ndb.Model):
    """
    Blog post database model
    """
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    user = ndb.KeyProperty(kind="User", required=True)
    likes = ndb.KeyProperty(kind="Like", repeated=True)
