import webapp2
from base import Main
from register import Register
from login import Login, Logout
from front import Front

args = [("/", Main),
        ("/login", Login),
        ("/logout", Logout),
        ("/register", Register),
        ("/([a-zA-Z0-9_]+)", Front)]

app = webapp2.WSGIApplication(args, debug = True)
