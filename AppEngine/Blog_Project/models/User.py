from google.appengine.ext import ndb
from models.Comment import Comment
from models.Post import Post
from models.Like import Like

class User(ndb.Model):
    """
    User database model
    """
    username = ndb.StringProperty(required=True)
    username_lower = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    comments = ndb.KeyProperty(kind=Comment, required=False, repeated=True)
    posts = ndb.KeyProperty(kind=Post, required=False, repeated=True)
    likes = ndb.KeyProperty(kind=Like, repeated=True)
