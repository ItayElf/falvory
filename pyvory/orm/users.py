import random
import sqlite3
from hashlib import md5
from string import printable

from pyvory.orm import DBConnect

SALT_LEN = 32


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
