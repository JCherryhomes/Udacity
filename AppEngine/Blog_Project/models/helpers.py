import re
import hashlib
import webapp2
import random
import string
import collections
from models.User import User

UserHash = collections.namedtuple('UserHash', ['user', 'hash'])

def valid_cookie(cookie):
    '''
    Cookie validation
    '''
    cookie_re = re.compile(r'.+=;\s*Path=/')
    return cookie and cookie_re.match(cookie)

def valid_username(username):
    '''
    Username validation
    '''
    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return user_re.match(username)

def valid_password(password):
    '''
    Password validation
    '''
    password_re = re.compile(r"^.{3,20}$")
    return password_re.match(password)

def valid_verify(password, verify):
    '''
    Validates that the password matches the verify password
    '''
    return valid_password(password) and password == verify

def valid_email(email):
    '''
    Simple email validation
    '''
    email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return not email or email_re.match(email)

def encrypt_password(password):
    '''
    Encrypts the password for storage in the datastore
    '''
    return hashlib.md5(password).hexdigest()

def make_salt():
    '''
    Creates a random salt
    '''
    return ''.join(random.choice(string.letters) for x in xrange(5))

def valid_pw(name, password, input_hash):
    '''
    uses the salt from the cookie to validate the users password
    '''
    try:
        salt = input_hash.split('|')[1]
        pw_hash = hashlib.sha256(name + password + salt).hexdigest()
        return input_hash == ('%s|%s' % (pw_hash, salt))
    except:
        return None

def make_pw_hash(name, pw):
    '''
    Creates the password hash
    '''
    salt = make_salt()
    pw_hash = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (pw_hash, salt)

def get_user_from_cookie(user_cookie):
    '''
    Returns the db instance of the user from the user
    cookie. If no cookie then None is returned
    '''
    if not user_cookie:
        return [None]
    else:
        strings = user_cookie.split('|')
        user_id = int(strings[0])
        user_hash = '%s|%s' % (strings[1], strings[2])

        return UserHash(User.get_by_id(user_id), user_hash)