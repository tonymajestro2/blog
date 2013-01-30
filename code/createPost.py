from base import BaseHandler, restricted_to_logged_in
from models import User, Post

class CreatePost(BaseHandler):
    def render(self, **errors):
        super(CreatePost, self).render("create_post.html", "Create Post", **errors)

    @restricted_to_logged_in
    def get(self):
        self.render()

    @restricted_to_logged_in
    def post(self):
        title = self.request.get("title")
        body = self.request.get("body").replace("\n", "<br>")

        if not (title and body):
            self.render_create_form(create_post_error = "Please enter a title and post")
        else:
            post = Post.register(user, title, body)
            post.put()
            self.redirect("/{0}".format(user.username))



