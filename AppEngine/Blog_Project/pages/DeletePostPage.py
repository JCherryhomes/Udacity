from models.Handler import Handler
from models.Post import Post
from models.Like import Like

def remove_user_post(user, post):
    '''
    removes the post from the user
    '''
    index = user.posts.index(post.key)
    user.posts.pop(index)
    user.put()

def remove_likes_for_post(post):
    '''
    removes the likes for the post
    '''
    likes = Like.query(Like.post == post.key)
    if likes:
        for like in likes.fetch():
            like.key.delete()

class DeletePostPage(Handler):
    '''
    Class for handling Like requests
    '''
    def post(self, post_id):
        '''
        Deletes the post if the current user
        was the author and the post exists
        '''
        current_user = self.authenticate_user()
        post = Post.get_by_id(long(post_id))

        if not current_user:
            self.redirect("/login")
        elif post.user != current_user.key:
            self.redirect(self.request.referer)
        elif post:
            remove_user_post(current_user, post)
            remove_likes_for_post(post)
            post.key.delete()
            self.redirect("/")
        else:
            self.render("post404.html")
