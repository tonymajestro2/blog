from base import BaseHandler
from models import User, Post

class CreatePost(BaseHandler):
    def render_create_form(self, **errors):
        self.render("create_post.html", "Create Post", **errors)

    def get(self):
        user = self.get_user()
        if not user:
            self.redirect("/login")
            return
        else:
            self.render_create_form()

    def post(self):
        user = self.get_user()
        if not user:
            self.redirect("/login")
            return 

        title = self.request.get("title")
        body = self.request.get("body").replace("\n", "<br>")

        if not (title and body):
            self.render_create_form(create_post_error = "Please enter a title and post")
        else:
            post = Post.register(user, title, body)
            post.put()
            self.redirect("/{0}".format(user.username))



