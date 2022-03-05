from pyvory.orm.connection import ROOT_PATH, DBConnect

if __name__ == '__main__':
    with DBConnect() as c:
        print(ROOT_PATH)
