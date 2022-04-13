import socket
from pyvory.orm.connection import DBConnect
from pyvory.orm.init import init_db
from web.setup import app

if __name__ == '__main__':
    with DBConnect() as c:
        init_db()
    if "liveconsole" not in socket.gethostname():
        app.run(debug=True, host="0.0.0.0")
