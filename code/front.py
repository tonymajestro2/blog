from base import BaseHandler, RestrictedToLoginHandler
from models import User, Post

class Front(RestrictedToLoginHandler):
    def render_posts(self, posts):
        html_list = []
        for p in posts:
            params = dict(title = p.title, created = p.created, body = p.body)
            html = self.get_html("post.html", **params)
            html_list.append(html)

        return "".join(html_list)

    def get(self):
        posts = self.user.posts.order("-created").run(limit = 10)
        posts_html = self.render_posts(posts)
        params = dict(posts = posts_html, username = self.user.username)
        self.render("front.html", self.user.username, **params)
