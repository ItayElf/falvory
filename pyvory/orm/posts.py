from typing import List

from pyvory.orm import DBConnect
from pyvory.social import Post

_get_feed = """SELECT u.name, r.id, r.author, r.title, r.description, r.steps, r.cooking_time, r.servings, 
GROUP_CONCAT(i.name, '~'), GROUP_CONCAT(i.quantity, '~'), GROUP_CONCAT(i.units, '~'), GROUP_CONCAT(u2.name, '~'), 
GROUP_CONCAT(c.content, '~'), GROUP_CONCAT(c."timestamp", '~'), GROUP_CONCAT(u3.name, '~'), GROUP_CONCAT(u4.name, '~'), 
p."timestamp", p.id, GROUP_CONCAT(f.followed_id), u.email, u.id
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
LEFT JOIN follows f ON f.follower_id = (SELECT id FROM users WHERE email=?)
GROUP BY p.id 
ORDER BY p."timestamp" DESC
LIMIT ? OFFSET ?"""


def get_feed(email: str, items: int, offset: int) -> List[Post]:
    """Returns a feed of a user"""
    with DBConnect() as c:
        c.execute(_get_feed, (email, items, offset))
        data = c.fetchall()
        if not data:
            raise Exception("No more posts")
        posts = [Post.from_tup(tup[:-3]) for tup in data if str(tup[-1]) in tup[-3].split(",") or tup[-2] == email]
        return posts
