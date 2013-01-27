import webapp2
from base import Main, Login
from register import Register

args = [("/", Main),
        ("/login", Login),
        ("/register", Register)]

app = webapp2.WSGIApplication(args, debug = True)
