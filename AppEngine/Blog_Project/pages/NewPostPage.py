from models.Handler import Handler
from models.Post import Post
import models.helpers as h

class NewPostPage(Handler):
    """
    Class for handling requests for creating a new blog post
    """
    def render_front(self, title="", content="", error=""):
        """
        Simplify the rendering of the new post template
        """
        current_user = self.authenticate_user()

        if not current_user:
            self.redirect("/login")
        else:
            self.render(
                "new_post.html",
                title=title,
                content=content,
                error=error,
                current_user=current_user)

    def get(self):
        """
        Render the new post template
        """
        self.render_front()

    def post(self):
        """
        Attempt to create a new blog post
        """
        current_user = self.authenticate_user()

        if not current_user:
            self.redirect("/login")
        else:
            content = self.request.get("content")
            title = self.request.get("subject")

            if not content or not title:
                self.render_front(title, content, "We need both a title and content")
            else:
                post = Post(title=title, content=content, user=current_user.key)
                post.put()

                current_user.posts.append(post.key)
                current_user.put()

                self.redirect("/post/" + str(post.key.id()))
