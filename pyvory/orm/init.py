from pyvory.orm import DBConnect

_init_script = """
CREATE TABLE IF NOT EXISTS ingredients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    quantity REAL NOT NULL,
    units text NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS recipes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author text NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    steps text NOT NULL,
    cooking_time INTEGER,
    servings text,
    image BLOB
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
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE(section_id, recipe_id)
);
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email text NOT NULL UNIQUE,
    password text NOT NULL,
    salt text NOT NULL,
    name text NOT NULL UNIQUE,
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
    FOREIGN KEY(section_id) REFERENCES sections(id) ON DELETE CASCADE,
    UNIQUE(cookbook_id, section_id)
);
CREATE TABLE IF NOT EXISTS comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    commenter_id INTEGER NOT NULL,
    content text NOT NULL,
    "timestamp" INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
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
CREATE TABLE IF NOT EXISTS follows(
    follower_id INTEGER NOT NULL,
    followed_id INTEGER NOT NULL,
    FOREIGN KEY(follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(followed_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(follower_id, followed_id)
);
CREATE TABLE IF NOT EXISTS likes(
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(post_id, user_id)
);
CREATE TABLE IF NOT EXISTS cooked(
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(post_id, user_id)
);
"""


def init_db():
    """Creates the tables for the db if they don't exist"""
    with DBConnect() as c:
        c.executescript(_init_script)
