from models.Handler import Handler
from models.Post import Post
from models.Like import Like

def remove_user_like(user, like):
    '''
    removes the like from the user
    '''
    index = user.likes.index(like.key)
    user.likes.pop(index)
    user.put()

def remove_post_like(post, like):
    '''
    removes the like from the post
    '''
    index = post.likes.index(like.key)
    post.likes.pop(index)
    post.put()

class LikePage(Handler):
    '''
    Class for handling Like requests
    '''
    def post(self, post_id):
        '''
        Adds or removes likes depending on if
        a like exists for the post
        by the current user and the current
        user did not write the post
        '''
        current_user = self.authenticate_user()
        post = Post.get_by_id(long(post_id))

        like = Like.query(
            Like.user == current_user.key,
            Like.post == post.key).get()

        if post.user == current_user.key:
            self.redirect(self.request.referer)
        elif like:
            remove_user_like(current_user, like)
            remove_post_like(post, like)
            like.key.delete()
        else:
            like = Like(user=current_user.key, post=post.key)
            like.put()

            post.likes.append(like.key)
            post.put()

            current_user.likes.append(like.key)
            current_user.put()

        self.redirect(self.request.referer)
