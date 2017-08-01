from models.Post import Post
from models.Handler import Handler

class MainPage(Handler):
    """
    Verify user
    redirect to signup if user does not exist
    otherwise load user's posts
    """
    def get(self):
        """
        If the user is logged in then render the existing blog posts
        """
        current_user = self.authenticate_user()
        posts = Post.query().fetch()

        if current_user:
            self.render(
                "main.html",
                posts=posts,
                current_user=current_user)
        else:
            self.render(
                "main.html",
                posts=posts)
