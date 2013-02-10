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



class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.user = self.get_user()

    def get_html(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(**params)

    def render(self, template, title, **params):
        params["title"] = title
        params["s"] = self
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

    def generate_header_links(self):
        links = []
        if self.get_user():
            links.append(("/settings", "Settings"))
            links.append(("/logout", "Logout"))
        else:
            links.append(("/register", "Register"))
            links.append(("/login", "Login"))

        return links


class RestrictedToLoginHandler(BaseHandler):
    """ Manages handlers whose methods are restricted to logged in users.
    If the user is logged in, it procedes to execute the handler's methods.
    Otherwise, it redirects the user to the login page.
    """
    def dispatch(self):
        if self.logged_in():
            super(RestrictedToLoginHandler, self).dispatch()
        else:
            self.redirect("/login")


class RestrictedToLogoutHandler(BaseHandler):
    """ Manages handlers whose methods are restricted to logged out users.
    If the user is logged out, it procedes to execute the handler's methods.
    Otherwise, it redirects the usre to their front page.
    """
    def dispatch(self):
        if not self.logged_in():
            super(RestrictedToLogoutHandler, self).dispatch()
        else:
            self.redirect("/blog")





