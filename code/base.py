import webapp2
import jinja2
import os
import utils
from models import User
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(
        loader = jinja2.FileSystemLoader(template_dir),
        autoescape = True)

def restricted_to_logged_in(method):
    """ Describes a method that should redirect to the login
    page if the user is not logged in. Otherwise, the method is
    executed.
    """
    def wrapper(self, *args, **kwargs):
        if self.logged_in():
            method(self, *args, **kwargs)
        else:
            self.redirect("/login")

    return wrapper


def restricted_to_logged_out(method):
    """ Describes a method that should redirect to the user's
    front page if they are already logged in. Otherwise, the
    method is executed.
    """
    def wrapper(self, *args, **kwargs):
        if self.logged_in():
            self.redirect("/{0}".format(self.user.username))
        else:
            method(self, *args, **kwargs)

    return wrapper


class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.user = self.get_user()

    def get_html(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(**params)

    def render(self, template, title, **params):
        params["title"] = title
        self.set_header_links(params)
        html_str = self.get_html(template, **params)
        self.response.out.write(html_str)

    def set_cookie(self, name, value):
        cookie = "{0}={1}; Path=/".format(name, value)
        self.response.headers.add_header("Set-Cookie", cookie)

    def read_cookie(self, name):
        return self.request.cookies.get(name)

    def login(self, user):
        user_id = str(user.key().id())
        value = utils.make_session_token(user_id)
        self.set_cookie("session_cookie", value)

    def logout(self):
        self.set_cookie("session_cookie", "")

    def logged_in(self):
        return self.user

    def get_user(self):
        user_id = self.validate_user()
        return user_id and User.get_by_id(user_id)

    def validate_user(self):
        token = self.read_cookie("session_cookie")
        return token and utils.validate_session_token(token)

    def set_header_links(self, params):
        if self.get_user():
            params["log_link"] = "/logout"
            params["log_text"] = "Logout"
        else:
            params["log_link"] = "/login"
            params["log_text"] = "Login"
            params["register_link"] = """<li><a href="/register">Register</a></li>"""

        return params










