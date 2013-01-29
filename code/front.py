from base import BaseHandler
from models import User, Post

class Front(BaseHandler):
    def render_posts(self, posts):
        html_list = []
        for p in posts:
            html = get_html(
                    "post.html",
                    title = p.title,
                    created = p.created,
                    body = p.body)

            html_list.append(html)
        return "".join(html_list)

    def get(self, username):
        user = self.get_user()
        if not (user and user.username == username):
            self.redirect("/")

        posts_html = self.render_posts(user.posts)
        self.render(
                "front.html", 
                username, 
                posts = posts_html, 
                username = username.capitalize())

