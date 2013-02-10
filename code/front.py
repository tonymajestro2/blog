from base import RestrictedToLoginHandler
from models import User, Post

class Front(RestrictedToLoginHandler):
    def render(self, user, page, **params):
        params["s"] = self
        super(Front, self).render(page, user.username, **params)

    def render_post(self, p):
        params = dict(title = p.title, created = p.created, body = p.body)
        return self.get_html("post.html", **params)

    def render_front(self):
        posts = self.user.posts.order("-created").run(limit = 10)
        params = dict(posts = posts, username = self.user.username, s = self)
        return self.get_html("front.html", **params)

    def get(self):
        self.render()


class PublicFront(Front):
    def get(self, username):
        user = User.get_by_name(username)
        if not (user and user.public):
            self.error(404)
            return

        self.render(user, "front_public.html")


class PrivateFront(Front):
    def get(self):
        self.render(self.user, "front_private.html")
