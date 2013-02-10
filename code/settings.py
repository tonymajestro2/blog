from base import RestrictedToLoginHandler
from models import User

class Settings(RestrictedToLoginHandler):
    def get(self):
        public = "checked" if self.user.public else ""
        self.render("settings.html", "Settings", public_checked = public)

    def post(self):
        public = self.request.get("public")
        if public:
            self.user.public = True
        else:
            self.user.public = False

        self.user.put()
        self.redirect("/blog")


