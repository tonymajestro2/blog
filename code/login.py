import utils
from base import BaseHandler, RestrictedToLogoutHandler
from models import User


class Login(RestrictedToLogoutHandler):
    def render_login(self, **errors):
        return self.get_html("login_form.html", **errors)

    def render(self, **errors):
        login_form = self.render_login(**errors)
        super(Login, self).render("login_page.html", "Login", login_form = login_form)

    def get(self):
        self.render()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        if not self._valid_login_credentials(username, password):
            self.render(login_error = "Invalid login")
        else:
            user = User.get_by_name(username)
            self.login(user)
            self.redirect("/blog")
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





