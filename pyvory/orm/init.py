from pyvory.orm import DBConnect

_init_script = """
CREATE TABLE IF NOT EXISTS ingredients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    quantity REAL NOT NULL,
    units text NOT NULL
);
CREATE TABLE IF NOT EXISTS recipes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author text NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    steps text NOT NULL,
    cooking_time INTEGER,
    servings INTEGER,
    image BLOB
);
CREATE TABLE IF NOT EXISTS ingredients_recipes(
    ingredient_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY(ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
    FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS sections(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    color text NOT NULL
);
CREATE TABLE IF NOT EXISTS sections_recipes(
    section_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY(section_id) REFERENCES sections(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL UNIQUE,
    password text NOT NULL,
    salt text NOT NULL,
    name text NOT NULL,
    bio text NOT NULL,
    link text NOT NULL,
    profile_pic BLOB
);
CREATE TABLE IF NOT EXISTS cookbooks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    creator_id INTEGER NOT NULL,
    bottom_title INTEGER NOT NULL,
    background_color text NOT NULL,
    font_color text NOT NULL,
    accent_color text,
    FOREIGN KEY(creator_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS cookbooks_sections(
    cookbook_id INTEGER NOT NULL,
    section_id INTEGER NOT NULL,
    FOREIGN KEY(cookbook_id) REFERENCES cookbooks(id) ON DELETE CASCADE,
    FOREIGN KEY(section_id) REFERENCES sections(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    commenter_id INTEGER NOT NULL,
    content text NOT NULL,
    "timestamp" INTEGER NOT NULL,
    FOREIGN KEY(commenter_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poster_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    "timestamp" INTEGER NOT NULL,
    FOREIGN KEY(poster_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS comments_posts(
    post_id INTEGER NOT NULL,
    comment_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(comment_id) REFERENCES comments(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS follows(
    follower_id INTEGER NOT NULL,
    followed_id INTEGER NOT NULL,
    FOREIGN KEY(follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(followed_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS likes(
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS cooked(
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""


def init_db():
    """Creates the tables for the db if they don't exist"""
    with DBConnect() as c:
        c.executescript(_init_script)
