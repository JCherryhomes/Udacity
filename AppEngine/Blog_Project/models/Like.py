from google.appengine.ext import ndb

class Like(ndb.Model):
    """
    Blog post database model
    """
    user = ndb.KeyProperty(kind="User", required=True)
    post = ndb.KeyProperty(kind="Post", required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
