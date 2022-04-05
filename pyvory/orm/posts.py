import random
import sqlite3
import time
from typing import List, Optional

from pyvory.orm import DBConnect
from pyvory.orm.recipes import insert_recipe
from pyvory.orm.users import get_user_by_email
from pyvory.social import Post, Comment

_get_posts = """
SELECT u.name, r.id, r.author, r.title, r.description, r.steps, r.cooking_time, r.servings, GROUP_CONCAT(i.name, '~'), 
GROUP_CONCAT(i.quantity, '~'), GROUP_CONCAT(i.units, '~'), GROUP_CONCAT(u2.name, '~'), GROUP_CONCAT(c.content, '~'), 
GROUP_CONCAT(c."timestamp", '~'), GROUP_CONCAT(u3.name, '~'), GROUP_CONCAT(u4.name, '~'), p."timestamp", p.id
FROM posts p
LEFT JOIN users u ON u.id = p.poster_id
LEFT JOIN recipes r ON r.id = p.recipe_id
LEFT JOIN ingredients i ON i.recipe_id = r.id  
LEFT JOIN comments c ON c.post_id = p.id 
LEFT JOIN users u2 ON u2.id = c.commenter_id 
LEFT JOIN likes l ON l.post_id = p.id 
LEFT JOIN users u3 ON u3.id = l.user_id 
LEFT JOIN cooked c2 ON c2.post_id = p.id 
LEFT JOIN users u4 ON u4.id = c2.user_id 
"""

_get_feed = """
WHERE u.id IN (SELECT f2.followed_id FROM follows f2 JOIN users u5 ON u5.id = f2.follower_id WHERE u5.email=?) OR u.email=?
GROUP BY p.id 
ORDER BY p."timestamp" DESC
LIMIT ? OFFSET ?;"""

_get_by_id = "WHERE p.id=?"

_get_by_name = """
WHERE u.name = ?
GROUP BY p.id 
ORDER BY p."timestamp" DESC;
"""

_get_cooked = """
WHERE u4.name = ?
GROUP BY p.id 
ORDER BY p."timestamp" DESC;
"""

_get_search = """
WHERE r.title LIKE ? OR r.description LIKE ? OR u.name LIKE ? 
GROUP BY p.id 
ORDER BY p."timestamp" DESC
"""

_get_explore = """
WHERE u.email != ? AND u.id NOT IN (SELECT followed_id FROM follows WHERE follower_id=(SELECT id FROM users WHERE email=?))
GROUP BY p.id 
ORDER BY p."timestamp" DESC
"""


def get_feed(email: str, items: int, offset: int) -> List[Post]:
    """Returns a feed of a user"""
    with DBConnect() as c:
        c.execute(_get_posts + _get_feed, (email, email, items, offset))
        data = c.fetchall()
        if not data:
            raise Exception("No more posts")
        posts = [Post.from_tup(tup) for tup in data]
        return posts


def get_post(idx: int) -> Post:
    """Returns a post by id"""
    with DBConnect() as c:
        c.execute(_get_posts + _get_by_id, (idx,))
        tup = c.fetchone()
        if not tup:
            raise Exception(f"No post with id {idx}")
        return Post.from_tup(tup)


def get_posts_of(name: str) -> List[Post]:
    """Returns all posts that were posted by given user"""
    with DBConnect() as c:
        c.execute(_get_posts + _get_by_name, (name,))
        lst = c.fetchall()
        return [Post.from_tup(tup) for tup in lst]


def get_cooked_by(name: str) -> List[Post]:
    """Returns all posts cooked by a user"""
    with DBConnect() as c:
        c.execute(_get_posts + _get_cooked, (name,))
        lst = c.fetchall()
        return [Post.from_tup(tup) for tup in lst]


def like(email: str, post_id: int) -> bool:
    """Like a post"""
    try:
        with DBConnect() as c:
            c.execute("INSERT INTO likes(post_id, user_id) VALUES(?, (SELECT id FROM users WHERE email=?))",
                      (post_id, email))
        return True
    except sqlite3.IntegrityError:
        raise Exception("User already likes the post")


def dislike(email: str, post_id: int) -> bool:
    """Removes a like from a post"""
    with DBConnect() as c:
        c.execute("DELETE FROM likes WHERE post_id=? AND user_id=(SELECT id FROM users WHERE email=?)",
                  (post_id, email))
        if c.rowcount == 0:
            raise Exception("User did not like the post")
        return True


def cooked(email: str, post_id: int) -> bool:
    """Marks a post as cooked"""
    try:
        with DBConnect() as c:
            c.execute("INSERT INTO cooked(post_id, user_id) VALUES(?, (SELECT id FROM users WHERE email=?))",
                      (post_id, email))
        return True
    except sqlite3.IntegrityError:
        raise Exception("User already cooked the post")


def uncooked(email: str, post_id: int) -> bool:
    """Marks a post as uncooked"""
    with DBConnect() as c:
        c.execute("DELETE FROM cooked WHERE post_id=? AND user_id=(SELECT id FROM users WHERE email=?)",
                  (post_id, email))
        if c.rowcount == 0:
            raise Exception("User did not cooked the post")
        return True


def comment(email: str, post_id: int, content: str) -> Comment:
    """Adds a comment on the post"""
    tstamp = int(time.time())
    try:
        with DBConnect() as c:
            c.execute(
                "INSERT INTO comments(post_id, commenter_id, content, \"timestamp\") VALUES(?, (SELECT id FROM users WHERE email=?), ?, ?)",
                (post_id, email, content, tstamp))
            c.execute("SELECT name FROM users WHERE email=?", (email,))
            tup = c.fetchone()
            return Comment(tup[0], content, tstamp)
    except sqlite3.IntegrityError:
        raise Exception(f"No user with email {email} was found")


def insert_post(email: str, p: Post, image: Optional[str] = None) -> Post:
    """Inserts a post end returns it back with correct id and timestamp"""
    tstamp = int(time.time())
    with DBConnect() as c:
        p.recipe = insert_recipe(p.recipe, image)
        c.execute(
            "INSERT INTO posts(id, poster_id, recipe_id, \"timestamp\") VALUES(?, (SELECT id FROM users WHERE email=?), ?, ?)",
            (p.recipe.idx, email, p.recipe.idx, tstamp))
        p.idx = p.recipe.idx
        p.timestamp = tstamp
        return p


def search_posts(query: str) -> List[Post]:
    """Returns all posts that match the recipe title, recipe description or poster name"""
    query = f"%{query}%"
    with DBConnect() as c:
        c.execute(_get_posts + _get_search, (query, query, query))
        return [Post.from_tup(tup) for tup in c.fetchall()]


def explore_posts(email: str, seed: int, items: int, offset: int) -> List[Post]:
    """Returns random posts"""
    with DBConnect() as c:
        c.execute(_get_posts + _get_explore, (email, email))
        posts = [Post.from_tup(tup) for tup in c.fetchall()]
        random.Random(seed).shuffle(posts)
        res = posts[offset: offset + items]
        if not res:
            raise Exception("No more posts")
        return res


def delete_post(email: str, idx: int) -> bool:
    """Deletes a post if email match the owner"""
    try:
        with DBConnect() as c:
            user = get_user_by_email(email)
            c.execute(
                "DELETE FROM recipes WHERE id=? AND (SELECT poster_id FROM posts WHERE id=?) = ?",
                (idx, idx, user.idx))
            c.execute("DELETE FROM ingredients WHERE recipe_id=? AND (SELECT poster_id FROM posts WHERE id=?) = ?",
                      (idx, idx, user.idx))
            c.execute("DELETE FROM posts WHERE poster_id=? AND id=?", (user.idx, idx))
            return True
    except FileNotFoundError:
        return False
