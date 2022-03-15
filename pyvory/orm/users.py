import random
import sqlite3
from hashlib import md5
from string import printable

from pyvory.orm import DBConnect
from pyvory.social import User

SALT_LEN = 32

_get_user = """
SELECT u.id, u.name, u.bio, u.link, GROUP_CONCAT(f1.followed_id), GROUP_CONCAT(f2.follower_id), GROUP_CONCAT(p.id), GROUP_CONCAT(c.id)
FROM users u
LEFT JOIN follows f1 ON f1.follower_id = u.id 
LEFT JOIN follows f2 ON f2.followed_id = u.id
LEFT JOIN posts p ON p.poster_id = u.id 
LEFT JOIN cookbooks c ON c.creator_id = u.id
"""


def login(email: str, password: str) -> bool:
    """Checks whether the user logged in successfully or not"""
    with DBConnect() as c:
        c.execute("SELECT password, salt FROM users WHERE email=?", (email,))
        tup = c.fetchone()
        if not tup:
            return False
        return md5((password + tup[1]).encode()).hexdigest() == tup[0]


def register(email: str, password: str, name: str):
    """Registers a user if there is not a user with this email yet"""
    salt = _generate_salt()
    password = md5((password + salt).encode()).hexdigest()
    with DBConnect() as c:
        try:
            c.execute("INSERT INTO users(email, password, salt, name, bio, link) VALUES(?,?,?,?,?,?)",
                      (email, password, salt, name, "", ""))
        except sqlite3.IntegrityError:  # email is taken
            raise Exception("A user with this email already exists")


def _generate_salt() -> str:
    """Returns a random string"""
    return "".join([random.choice(printable) for _ in range(SALT_LEN)])


def get_user_by_email(email: str):
    with DBConnect() as c:
        c.execute(_get_user + "WHERE u.email = ?", (email,))
        tup = c.fetchone()
        if not tup or not tup[0]:
            raise FileNotFoundError(f"User with email '{email}' was not found")
        return User.from_tup(tup)
