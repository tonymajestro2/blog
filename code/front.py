from base import BaseHandler
from models import User, Post

class Front(BaseHandler):
    def render_posts(self, posts):
        html_list = []
        for p in posts:
            params = dict(title = p.title, created = p.created, body = p.body)
            html = self.get_html("post.html", **params)
            html_list.append(html)

        return "".join(html_list)

    def get(self, username):
        user = self.get_user()
        if not (user and user.username == username):
            self.redirect("/login")
            return

        posts = user.posts.order("-created").run(limit = 10)
        posts_html = self.render_posts(posts)
        params = dict(posts = posts_html, username = username)
        self.render("front.html", username, **params)

