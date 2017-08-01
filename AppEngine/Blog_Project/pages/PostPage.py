from models.Handler import Handler
from models.Post import Post
from models.User import User
from models.Comment import Comment
from models.Like import Like
import models.helpers as h
import time

class PostPage(Handler):
    """
    Displays the content of a blog post
    """
    def get(self, post_id):
        """
        Renders the post.html template with the requested post
        """
        current_user = self.authenticate_user()

        if not post_id:
            self.render("post.html", error="No post id provided")
        else:
            post = Post.get_by_id(long(post_id))

            if not post:
                self.render("post404.html")
            else:
                user = User.get_by_id(post.user.id())
                comments = Comment.query().filter(Comment.post == post.key).fetch()
                likes = Like.query(Like.post == post.key).fetch()
                like = Like.query(
                    Like.user == current_user.key,
                    Like.post == post.key).get()

                self.render(
                    "post.html",
                    post=post,
                    current_user=current_user,
                    user=user,
                    like_count = len(likes),
                    like=like,
                    comments=comments)

    def post(self, post_id):
        """
        Handles the post request from the post page. This is the comment submission.
        """
        content = self.request.get("content")
        current_user = self.authenticate_user()

        post = Post.get_by_id(long(post_id))
        user = User.get_by_id(post.user.id())
        comments = Comment.query().filter(Comment.post == post.key).fetch()

        if not content:
            self.render("post.html",
                comments=comments,
                post=post,
                current_user=current_user,
                user=user,
                error="No comment text was received")
        else:
            comment = Comment(content=content, user=current_user.key, post=post.key)
            comment.put()
            current_user.comments.append(comment.key)
            current_user.put()
            timestamp = str(time.time()).replace(".","")

            self.render(
                "post.html",
                post=post,
                user=user,
                current_user=current_user,
                comments=comments)
