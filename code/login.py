import utils
from base import BaseHandler
from models import User


class Login(BaseHandler):
    def render_login(self):
        return self.get_html("login.html")

    def render_page(self, **params):
        if params == None:
            params = {}

        params["s"] = self
        self.render("login_page.html", "Login", **params)

    def get(self):
        self.render_page()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        if not self._valid_login_credentials(username, password):
            self.render_page(login_error = "Invalid login")
        else:
            user = User.get_by_name(username)
            self.login(user)
            self.redirect("/")

    def _valid_login_credentials(self, username, password):
        user = User.get_by_name(username)
        if not user:
            return False

        h = user.pw_hash
        return utils.verify_pw(username, password, h)


class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect("/")





