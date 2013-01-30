from base import BaseHandler

class Main(BaseHandler):
    def render(self, **params):
        super(Main, self).render("main.html", "Tiny Blogs", **params)


    def get(self):
        user = self.get_user()
        if user:
            self.redirect("/{0}".format(user.username))
            return
        else:
            login_form = self.get_html("login_form.html")
            self.render(login_form = login_form)




