import webapp2
from base import Main
from register import Register
from login import Login, Logout

args = [("/", Main),
        ("/login", Login),
        ("/logout", Logout),
        ("/register", Register)]

app = webapp2.WSGIApplication(args, debug = True)
