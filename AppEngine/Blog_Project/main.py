import webapp2
import sys
from pages.MainPage import MainPage
from pages.LoginPage import LoginPage
from pages.LogoutPage import LogoutPage
from pages.SignupPage import SignupPage
from pages.NewPostPage import NewPostPage
from pages.PostPage import PostPage
from pages.EditPostPage import EditPostPage
from pages.EditCommentPage import EditCommentPage
from pages.LikePage import LikePage
from pages.CommentPage import CommentPage
from pages.DeletePostPage import DeletePostPage

sys.path.append('/models')
sys.path.append('/pages')

app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/signup", SignupPage),
    ("/login", LoginPage),
    ("/logout", LogoutPage),
    ("/newpost", NewPostPage),
    ("/post/(\d+)", PostPage),
    ("/editpost/(\d+)", EditPostPage),
    ("/editcomment/(\d+)", EditCommentPage),
    ("/like/(\d+)", LikePage),
    ("/comment/(\d+)", CommentPage),
    ("/deletepost/(\d+)", DeletePostPage)], debug=True)

app.config['TEMPLATES_AUTO_RELOAD'] = True