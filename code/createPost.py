from base import BaseHandler, RestrictedToLoginHandler
from models import User, Post

class CreatePost(RestrictedToLoginHandler):
    def render(self, **errors):
        super(CreatePost, self).render("create_post.html", "Create Post", **errors)

    def get(self):
        self.render()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body").replace("\n", "<br>")

        if not (title and body):
            self.render_create_form(create_post_error = "Please enter a title and post")
        else:
            post = Post.register(self.user, title, body)
            post.put()
            self.redirect("/blog")



