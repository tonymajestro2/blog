import webapp2
from base import Main
from register import Register
from login import Login

args = [("/", Main),
        ("/login", Login),
        ("/register", Register)]

app = webapp2.WSGIApplication(args, debug = True)
