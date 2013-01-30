from base import BaseHandler, restricted_to_logged_in
from models import User, Post

class Front(BaseHandler):
    def render_posts(self, posts):
        html_list = []
        for p in posts:
            params = dict(title = p.title, created = p.created, body = p.body)
            html = self.get_html("post.html", **params)
            html_list.append(html)

        return "".join(html_list)

    @restricted_to_logged_in
    def get(self):
        posts = self.user.posts.order("-created").run(limit = 10)
        posts_html = self.render_posts(posts)
        params = dict(posts = posts_html, username = self.user.username)
        self.render("front.html", self.user.username, **params)

    def _visiting_own_blog(self, username):
        return self.user.username == username
