import base64
import random
import sqlite3
import zlib
from hashlib import md5
from string import printable
from typing import List, Tuple, Optional

from pyvory.orm import DBConnect
from pyvory.orm.utils import image_to_webp
from pyvory.social import User

SALT_LEN = 32
_blank_profile = open("pyvory/orm/blank_profile.png", "rb").read()

_get_user = """
SELECT u.id, u.name, u.bio, u.link, GROUP_CONCAT(u2.name), GROUP_CONCAT(u3.name), GROUP_CONCAT(p.id), GROUP_CONCAT(c.id)
FROM users u
LEFT JOIN follows f1 ON f1.follower_id = u.id 
LEFT JOIN follows f2 ON f2.followed_id = u.id
LEFT JOIN users u2 ON f1.followed_id = u2.id
LEFT JOIN users u3 ON f2.follower_id = u3.id
LEFT JOIN posts p ON p.poster_id = u.id 
LEFT JOIN cookbooks c ON c.creator_id = u.id
"""

_get_suggestions = """
SELECT u2.name, u3.name 
FROM users u 
JOIN follows f ON f.follower_id = u.id 
JOIN users u2 ON f.followed_id = u2.id 
JOIN follows f2 ON f2.follower_id = u2.id 
JOIN users u3 ON u3.id = f2.followed_id 
WHERE u.email=? AND u3.email != u.email AND u.id NOT IN (SELECT f3.follower_id FROM follows f3 WHERE f3.followed_id = u3.id)
ORDER BY RANDOM()
LIMIT 4;
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


def get_user_by_email(email: str) -> User:
    """Returns a user object based on its email"""
    with DBConnect() as c:
        c.execute(_get_user + "WHERE u.email = ?", (email,))
        tup = c.fetchone()
        if not tup or not tup[0]:
            raise FileNotFoundError(f"User with email '{email}' was not found")
        return User.from_tup(tup)


def get_user_by_name(name: str) -> User:
    """Returns a user object based on its email"""
    with DBConnect() as c:
        c.execute(_get_user + "WHERE u.name = ?", (name,))
        tup = c.fetchone()
        if not tup or not tup[0]:
            raise FileNotFoundError(f"User with name '{name}' was not found")
        return User.from_tup(tup)


def get_profile_pic(idx: int) -> bytes:
    """Returns the profile picture of a user if it has one, otherwise returns the base picture"""
    with DBConnect() as c:
        c.execute("SELECT profile_pic FROM users WHERE id = ?", (idx,))
        tup = c.fetchone()
        if not tup:
            raise FileNotFoundError(f"No user with id {idx} was found")
        elif not tup[0]:
            return _blank_profile
        else:
            return zlib.decompress(tup[0])


def get_profile_pic_by_name(name: str) -> bytes:
    """Returns the profile picture of a user if it has one, otherwise returns the base picture"""
    with DBConnect() as c:
        c.execute("SELECT profile_pic FROM users WHERE name = ?", (name,))
        tup = c.fetchone()
        if not tup:
            raise FileNotFoundError(f"No user with name {name} was found")
        elif not tup[0]:
            return _blank_profile
        else:
            return zlib.decompress(tup[0])


def get_suggestions(email: str) -> List[Tuple[str, str]]:
    """Returns (up to) 4 random suggestion to follow, where the first item in the tuple is the name of the user followed by the current user and the second item is the name of the suggested user"""
    with DBConnect() as c:
        c.execute(_get_suggestions, (email,))
        lst = c.fetchall()
        return lst


def follow(email: str, name: str) -> bool:
    """Adds a user as a follower of the other one"""
    try:
        with DBConnect() as c:
            c.execute(
                "INSERT INTO follows(follower_id, followed_id) VALUES((SELECT id FROM users WHERE email=?), (SELECT id FROM users WHERE name=?))",
                (email, name))
        return True
    except sqlite3.IntegrityError:
        raise Exception(f"User already follows {name}")


def unfollow(email: str, name: str) -> bool:
    """Removes a user from the followers of the other user"""
    with DBConnect() as c:
        c.execute(
            "DELETE FROM follows WHERE follower_id=(SELECT id FROM users WHERE email=?) AND followed_id=(SELECT id FROM users WHERE name=?)",
            (email, name))
        if c.rowcount == 0:
            raise Exception(f"User did not followed {name}")
        return True


def search_users(query: str, items: int, offset: int) -> List[User]:
    """Returns all users with name that matches the query"""
    query = f"%{query}%"
    with DBConnect() as c:
        c.execute(_get_user + "WHERE u.name LIKE ? GROUP BY u.id LIMIT ? OFFSET ?", (query, items, offset))
        res = [User.from_tup(tup) for tup in c.fetchall()]
        if not res:
            raise Exception("No more posts")
        return res


def update_user(email: str, name: str, bio: str, link: str, image: Optional[str] = None) -> None:
    """Updates the user to the given user"""
    with DBConnect() as c:
        if image is not None:
            if image:
                image = zlib.compress(image_to_webp(base64.b64decode(image)))
            else:
                image = None
        else:
            image = c.execute("SELECT profile_pic FROM users WHERE email=?", (email,)).fetchone()[0]
        c.execute("UPDATE users SET name=?, bio=?, link=?, profile_pic=? WHERE email=?",
                  (name, bio, link, image, email))
