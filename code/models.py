import utils
from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty(required = True)

    @classmethod
    def register(cls, username, password, email):
        pw_hash = utils.make_pw_hash(username, password)
        user = User(username = username,
                    pw_hash = pw_hash,
                    email = email)
        return user

    @classmethod
    def get_by_name(cls, username):
        user = User.all().filter("username =", username)
        return user.get()

    @classmethod
    def get_by_email(cls, email):
        user = User.all().filter("email =", email)
        return user.get()

    @classmethod
    def get_by_id(cls, user_id):
        key = db.Key.from_path("User", int(user_id))
        return key and db.get(key)


class Post(db.Model):
    user = db.ReferenceProperty(User, collection_name="posts", required = True)
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def register(cls, user, title, body):
        return Post(user = user, title = title, body = body)




