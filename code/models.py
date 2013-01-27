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

