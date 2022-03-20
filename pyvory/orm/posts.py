import sqlite3
from typing import List

from pyvory.orm import DBConnect
from pyvory.social import Post

_get_feed = """
SELECT u.name, r.id, r.author, r.title, r.description, r.steps, r.cooking_time, r.servings, GROUP_CONCAT(i.name, '~'), 
GROUP_CONCAT(i.quantity, '~'), GROUP_CONCAT(i.units, '~'), GROUP_CONCAT(u2.name, '~'), GROUP_CONCAT(c.content, '~'), 
GROUP_CONCAT(c."timestamp", '~'), GROUP_CONCAT(u3.name, '~'), GROUP_CONCAT(u4.name, '~'), p."timestamp", p.id
FROM posts p
LEFT JOIN users u ON u.id = p.poster_id
LEFT JOIN recipes r ON r.id = p.recipe_id
LEFT JOIN ingredients i ON i.recipe_id = r.id 
LEFT JOIN comments_posts cp ON cp.post_id = p.id 
LEFT JOIN comments c ON cp.comment_id = c.id 
LEFT JOIN users u2 ON u2.id = c.commenter_id 
LEFT JOIN likes l ON l.post_id = p.id 
LEFT JOIN users u3 ON u3.id = l.user_id 
LEFT JOIN cooked c2 ON c2.post_id = p.id 
LEFT JOIN users u4 ON u4.id = c2.user_id 
WHERE u.id IN (SELECT f2.followed_id FROM follows f2 JOIN users u5 ON u5.id = f2.follower_id WHERE u5.email=?) OR u.email=?
GROUP BY p.id 
ORDER BY p."timestamp" DESC
LIMIT ? OFFSET ?;
"""


def get_feed(email: str, items: int, offset: int) -> List[Post]:
    """Returns a feed of a user"""
    print(f"{items=}, {offset=}")
    with DBConnect() as c:
        c.execute(_get_feed, (email, email, items, offset))
        data = c.fetchall()
        if not data:
            raise Exception("No more posts")
        posts = [Post.from_tup(tup) for tup in data]
        return posts


def like(email: str, post_id: int) -> None:
    """Like a post"""
    try:
        with DBConnect() as c:
            c.execute("INSERT INTO likes(post_id, user_id) VALUES(?, (SELECT id FROM users WHERE email=?))",
                      (post_id, email))
    except sqlite3.IntegrityError:
        raise Exception("User already likes the post")


def dislike(email: str, post_id: int) -> None:
    """Removes a like from a post"""
    with DBConnect() as c:
        c.execute("DELETE FROM likes WHERE post_id=? AND user_id=(SELECT id FROM users WHERE email=?)",
                  (post_id, email))
        if c.rowcount == 0:
            raise Exception("User did not like the post")
