from base import RestrictedToLoginHandler
from models import User

class Settings(RestrictedToLoginHandler):
    def get(self):
        yes_checked = no_checked = ""
        if self.user.public:
            yes_checked = "checked"
        else:
            no_checked = "checked"

        self.render(
                "settings.html",
                "Settings",
                yes_checked = yes_checked,
                no_checked = no_checked)

    def post(self):
        public = self.request.get("public") == "yes"
        if public != self.user.public:
            self.user.public = public
            self.user.put()

        self.redirect("/blog")


