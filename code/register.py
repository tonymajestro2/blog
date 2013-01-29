import re
from models import User
from base import BaseHandler

USERNAME_RE = r"^[a-zA-Z0-9_]{3,16}$"
def valid_username(username):
    """ Valid usernames are 3-16 characters, using only letters, numbers, or
        userscore characters. """
    user_re = re.compile(USERNAME_RE)
    return user_re.match(username)

def valid_password(password):
    """ Valid passwords are at least 4 characters using letters or numbers. """
    pw_re = re.compile("^[a-zA-Z0-9]{4,20}$")
    return pw_re.match(password)

def valid_email(email):
    email_re = re.compile("^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+")
    return email_re.match(email)


class Register(BaseHandler):
    def get(self):
        self.render("register.html", "Register")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        errors = self._verify_user(username, password, verify, email)
        if errors:
            self.render("register.html", "Register", **errors)
        else:
            user = User.register(username, password, email)
            user.put()
            self.redirect("/")

    def _verify_user(self, username, password, verify, email):
        errors = {}

        if not (username and valid_username(username)):
            errors["username_error"] = "* Invalid username"
        elif self._username_exists(username):
            errors["username_error"] = "* Username already taken"

        if not (password and valid_password(password)):
            errors["password_error"] = "* Invalid password"
        elif password != verify:
            errors["verify_error"] = "* Passwords must match"

        if not email:
            errors["email_error"] = "* Invalid email"
        elif not valid_email(email):
            errors["email_error"] = "* Invalid email"
        elif self._email_exists(email):
            errors["email_error"] = "* Email already used"

        if errors:
            errors["username"] = username
            errors["email"] = email

        return errors

    def _username_exists(self, username):
        return User.get_by_name(username)

    def _email_exists(self, email):
        return User.get_by_email(email)

