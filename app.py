from pyvory.orm.connection import DBConnect
from pyvory.orm.init import init_db

if __name__ == '__main__':
    with DBConnect() as c:
        init_db()
