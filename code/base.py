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
    def set_log_links(self, params):
        if self.logged_in():
            params["log_link"] = "/logout"
            params["log_text"] = "Logout"
        else:
            params["log_link"] = "/login"
            params["log_text"] = "Login"

        return params

    def get_html(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(**params)

    def render(self, template, title, **params):
        if params == None:
            params = {}

        params["title"] = title
        self.set_log_links(params)
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
        return self.validate_user()

    def validate_user(self):
        token = self.read_cookie("session_cookie")
        return token and utils.validate_session_token(token)


class Main(BaseHandler):
    def get(self):
        login_form = self.get_html("login.html")
        self.render("main.html", "Blog", login_form = login_form)




