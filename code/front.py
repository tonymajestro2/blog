from base import RestrictedToLoginHandler, BaseHandler
from models import User, Post

class PrivateFront(RestrictedToLoginHandler):
    def render(self, **params):
        params["s"] = self
        super(PrivateFront, self).render("front_private.html", self.user.username, **params)

    def render_post(self, p):
        params = dict(title = p.title, created = p.created, body = p.body)
        return self.get_html("post.html", **params)

    def render_front(self):
        posts = self.user.posts.order("-created").run(limit = 10)
        params = dict(posts = posts, username = self.user.username, s = self)
        return self.get_html("front.html", **params)

    def get(self):
        self.render()


class PublicFront(BaseHandler):
    def render(self, user, **params):
        params["s"] = self
        params["user"] = user
        super(PublicFront, self).render("front_public.html", user.username, **params)

    def get(self, username):
        user = User.get_by_name(username)
        if not (user and user.public):
            self.error(404)
            return

        self.render(user)

    def render_post(self, p):
        params = dict(title = p.title, created = p.created, body = p.body)
        return self.get_html("post.html", **params)

    def render_front(self, user):
        posts = user.posts.order("-created").run(limit = 10)
        params = dict(posts = posts, username = user.username, s = self)
        return self.get_html("front.html", **params)

