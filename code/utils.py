import hashlib
import hmac
import random
import string
from secret import SECRET


# Password stuff
def make_salt(length):
    """ Make a salt of the given length for use in password hashing """
    return ''.join([random.choice(string.letters) for x in range(length)])

def make_pw_hash(username, password, salt = None):
    """ Make a hash from username, password, and optional salt
    Use a combination of username, password, and salt as input to the
    hash.  This hash is combined with the salt to be stored in the 
    database. 
    """
    if not salt:
        salt = make_salt(32)

    h = hashlib.sha256("{0}{1}{2}".format(username, password, salt)).hexdigest()
    return "{0}|{1}".format(h, salt)

def verify_pw(username, password, h):
    """ Verify username and password
    Given a username and password, generate a hash and compare it
    to the hash stored in the database. 
    """
    parts = h.split("|")
    if len(parts) != 2:
        return False

    salt = parts[1]
    return h == make_pw_hash(username, password, salt)

# Cookies stuff
def hash_str(s):
    """ Create a hash using the secret key for use in session tokens. """
    return hmac.new(SECRET, s).hexdigest()

def make_session_token(id_val):
    """ Combine the string s with its hash to create a secure value to be
    used in a session token. 
    """
    h = hash_str(id_val)
    return "{0}|{1}".format(id_val, h)

def validate_session_token(token):
    """ Validates session token string
    Session token contains two parts: the id and its hash.  To validate, use
    the given id extracted from the token to create a new session token value
    and compare it to the given token.
    """
    id_val = token.split("|")[0]
    return token == make_session_token(id_val)








