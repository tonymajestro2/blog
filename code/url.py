import webapp2
from main import Main
from register import Register
from login import Login, Logout
from front import Front
from createPost import CreatePost

args = [("/", Main),
        ("/login", Login),
        ("/logout", Logout),
        ("/register", Register),
        ("/createPost", CreatePost),
        ("/blog", Front)]

app = webapp2.WSGIApplication(args, debug = True)
