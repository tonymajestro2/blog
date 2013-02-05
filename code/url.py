import webapp2
from main import Main
from register import Register
from login import Login, Logout
from front import PublicFront, PrivateFront
from createPost import CreatePost
from settings import Settings

args = [("/", Main),
        ("/login", Login),
        ("/logout", Logout),
        ("/register", Register),
        ("/createPost", CreatePost),
        ("/blog", PrivateFront),
        ("/settings", Settings),
        ("/users/([a-zA-Z0-9_]{3,16})", PublicFront)]

app = webapp2.WSGIApplication(args, debug = True)
