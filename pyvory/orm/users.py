from pyvory.orm import DBConnect


def login(email: str, password: str) -> bool:
    """Checks whether the user logged in successfully or not"""
    with DBConnect() as c:
        c.execute("SELECT name FROM users WHERE email=? AND password=?", (email, password))  # TODO: add salt
        tup = c.fetchone()
        return not not tup
