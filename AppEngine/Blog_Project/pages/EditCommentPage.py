from models.Handler import Handler
from models.Post import Post
from models.User import User
from models.Comment import Comment
import models.helpers as h

class EditCommentPage(Handler):
    """
    Class for handling requests for creating a new blog post
    """
    def render_front(self, comment_id="", content="", error=""):
        """
        Simplify the rendering of the new post template
        """
        current_user = self.authenticate_user()
        comment = Comment.get_by_id(long(comment_id))
        user = User.get_by_id(comment.user.id())

        if not content:
            content = comment.content

        if not current_user:
            self.redirect("/login")
        elif current_user.key != comment.user:
            self.write("You are not the author of this comment")
        else:
            self.render(
                "edit_comment.html",
                content=content,
                error=error,
                user=user,
                current_user=current_user)

    def get(self, comment_id):
        """
        Render the new post template
        """
        self.render_front(comment_id)

    def post(self, comment_id):
        """
        Attempt to create a new blog post
        """
        current_user = self.authenticate_user()

        if not current_user:
            self.redirect("/login")
        else:
            content = self.request.get("content")
            comment = Comment.get_by_id(long(comment_id))

            if not comment:
                self.redirect("/post/" + str(comment.post.id()))
            elif current_user.key != comment.user:
                self.redirect("/post/" + str(comment.post.id()))
            elif not content:
                self.render_front(comment_id, content, "Your comment does not contain any content.")
            else:
                comment.content = content
                comment.put()

                self.redirect("/post/" + str(comment.post.id()))
