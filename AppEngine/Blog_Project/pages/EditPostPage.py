from models.Handler import Handler
from models.Post import Post
from models.User import User
import models.helpers as h

class EditPostPage(Handler):
    """
    Class for handling requests for creating a new blog post
    """
    def render_front(self, post_id="", error=""):
        """
        Simplify the rendering of the new post template
        """
        current_user = self.authenticate_user()
        post = Post.get_by_id(long(post_id))

        if not current_user:
            self.redirect("/login")
        elif not post:
            self.render("/post404.html")
        elif current_user.key != post.user:
            self.write("You are not the author of this post")
        else:
            user = post.user.id()
            self.render(
                "edit_post.html",
                title=post.title,
                content=post.content,
                error=error,
                current_user=current_user,
                user=user,
                post_id=post_id)

    def get(self, post_id):
        """
        Render the new post template
        """
        self.render_front(post_id)

    def post(self, post_id):
        """
        Attempt to create a new blog post
        """
        current_user = self.authenticate_user()

        if not current_user:
            self.redirect("/login")
        else:
            content = self.request.get("content")
            title = self.request.get("subject")

            post = Post.get_by_id(long(post_id))

            if not post:
                self.render("/post404.html")
            elif current_user.key != post.user:
                self.redirect("/post/" + str(post.key.id()))
            elif not content or not title:
                self.render_front(post_id, error="We need both a title and content")
            else:
                post.title = title
                post.content = content

                post.put()

                self.redirect("/post/" + str(post.key.id()))
