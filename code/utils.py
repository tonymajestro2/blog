import hashlib
import random
import string


def make_salt(length):
    return ''.join([random.choice(string.letters) for x in range(length)])

# Password stuff
def make_pw_hash(username, password, salt = None):
    if not salt:
        salt = make_salt(32)

    h = hashlib.sha256("{0}{1}{2}".format(username, password, salt)).hexdigest()
    return "{0}|{1}".format(h, salt)

def verify_pw(username, password, h):
    parts = h.split("|")
    if len(parts) != 2:
        return False

    salt = parts[1]
    return h == make_pw_hash(username, password, salt)

