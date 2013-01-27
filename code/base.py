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
    def render(self, template, title, **params):
        t = jinja_env.get_template(template)
        params["title"] = title
        html_str = t.render(params)
        self.response.out.write(html_str)


class Main(BaseHandler):
    def get(self):
        self.render("base.html", "Blog")




