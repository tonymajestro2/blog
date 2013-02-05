from base import BaseHandler, RestrictedToLoginHandler
from models import User, Post

class Front(RestrictedToLoginHandler):
    def render(self, **params):
        posts = self.user.posts.order("-created").run(limit = 10)
        posts_html = self.render_posts(posts)
        params["posts"] = posts_html
        params["username"] = self.user.username
        super(Front, self).render("front.html", self.user.username, **params)

    def render_posts(self, posts):
        html_list = []
        for p in posts:
            params = dict(title = p.title, created = p.created, body = p.body)
            html = self.get_html("post.html", **params)
            html_list.append(html)

        return "".join(html_list)

    def get(self):
        self.render()

class PublicFront(Front):

    def get(self, username):
        user = User.get_by_name(username)
        if not (user and user.public):
            self.error(404)
            return

        self.render(user = user)


class PrivateFront(Front):
    def get(self):
        create_button = self.get_html("front_button.html")
        self.render(createButton = create_button)
