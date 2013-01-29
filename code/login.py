import utils
from base import BaseHandler
from models import User


class Login(BaseHandler):
    def render_login(self, **errors):
        return self.get_html("login_form.html", **errors)

    def render_page(self, **errors):
        login_form = self.render_login(**errors)
        self.render("login_page.html", "Login", login_form = login_form)

    def get(self):
        user = self.get_user()
        if user:
            self.redirect("/{0}".format(user.username))
            return
        else:
            self.render_page()

    def post(self):
        user = self.get_user()
        if user:
            self.redirect("/{0}".format(user.username))
            return

        username = self.request.get("username")
        password = self.request.get("password")

        if not self._valid_login_credentials(username, password):
            self.render_page(login_error = "Invalid login")
        else:
            user = User.get_by_name(username)
            self.login(user)
            self.redirect("/{0}".format(username))
            return

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
        return





