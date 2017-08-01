from models.Handler import Handler
from models.Comment import Comment

def remove_user_comment(user, comment):
    '''
    removes the comment from the user
    '''
    index = user.comments.index(comment.key)
    user.comments.pop(index)
    user.put()

class CommentPage(Handler):
    '''
    Class for handling Comment requests
    '''
    def post(self, comment_id):
        '''
        Deletes the comment if the current
        user is the author of the comment
        '''
        current_user = self.authenticate_user()
        comment = Comment.get_by_id(long(comment_id))

        if comment and comment.user == current_user.key:
            remove_user_comment(current_user, comment)
            comment.key.delete()

        self.redirect(self.request.referer)
