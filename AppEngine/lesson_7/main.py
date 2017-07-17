import os
import webapp2
import hashlib
import hmac

SECRET = 'imsosecret'

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5)

def make_pw_hash(name, pw):
	salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s|%s' % (h, salt)

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

# -----------------
# User Instructions
# 
# Implement the function check_secure_val, which takes a string of the format 
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None 

def check_secure_val(response, h):
	strings = h.split("|")

	if not len(strings) == 2:
		return None

	val = strings[0]
	hash = strings[1]
	if hash == hash_str(val):
		return val

class MainPage(webapp2.RequestHandler):
	def get(self):
		visit_cookie = self.request.cookies.get('visits')
		visits = 0

		if visit_cookie:
			cookie_val = check_secure_val(self.response, visit_cookie)

			if cookie_val:
				visits = int(cookie_val)

		visits += 1

		self.response.headers.add_header('Set-Cookie', 'visits=%s' % make_secure_val(str(visits)))

		if visits > 10000:
			self.response.out.write("You are the best ever!")
		else:
			self.response.out.write("You have visited %s times" % visits)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)