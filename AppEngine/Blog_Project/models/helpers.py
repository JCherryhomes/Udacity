import re
import hashlib
import webapp2
import random
import string
import collections
from models.User import User

SECRET = 'imsosecret'
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
COOKIE_RE = re.compile(r'.+=;\s*Path=/')


UserHash = collections.namedtuple('UserHash', ['user', 'hash'])

def valid_cookie(cookie):
    return cookie and COOKIE_RE.match(cookie)

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_verify(password, verify):
    return valid_password(password) and password == verify

def valid_email(email):
    return not email or EMAIL_RE.match(email)

def encrypt_password(password):
    return hashlib.md5(password).hexdigest()

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def valid_pw(name, pw, h):
    try:
        salt = h.split('|')[1]
        hash = hashlib.sha256(name + pw + salt).hexdigest()
        return h == ('%s|%s' % (hash, salt))
    except:
        return None

def make_pw_hash(name, pw):
    salt = make_salt()
    pw_hash = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (pw_hash, salt)

def get_user_from_cookie(user_cookie):
    if not user_cookie:
        return [None]
    else:
        strings = user_cookie.split('|')
        id = int(strings[0])
        hash = '%s|%s' % (strings[1], strings[2])

        return UserHash(User.get_by_id(id), hash)