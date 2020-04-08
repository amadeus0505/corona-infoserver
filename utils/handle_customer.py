import sqlite3
import re
import hashlib

db_path = ""


def setup(path):
    global db_path
    db_path = path


def get_cursor():
    with sqlite3.connect(db_path) as db_conn:
        db_cursor = db_conn.cursor()
    return db_cursor


def get_conn():
    with sqlite3.connect(db_path) as db_conn:
        return db_conn


def is_empty(obj):
    typ = type(obj)
    if typ == str:
        obj = re.sub(r"\W", "", obj)
        if obj == "":
            return True
    elif typ == list or typ == set or typ == tuple:
        if len(obj) == 0:
            return True
    else:
        raise TypeError("cannot get emptiness of type " + str(typ))


def encrypted_pwd(pwd: str):
    return hashlib.sha256(pwd.encode()).hexdigest()


def user_exists(username: str):
    cursor = get_cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    rows = cursor.fetchall()
    print(rows)
    if is_empty(rows):
        return False
    return True


def login(username, pwd):
    cursor = get_cursor()
    cursor.execute(f"SELECT password FROM users WHERE username='{username}'")
    rows = cursor.fetchall()
    if is_empty(rows):
        return False
    elif rows[0][0] == encrypted_pwd(pwd):
        return True
    else:
        return False


def signup(username, name, pwd):
    conn = get_conn()
    cursor = conn.cursor()
    pwd = encrypted_pwd(pwd)
    cursor.execute(f"INSERT INTO users VALUES ('{username}', '{name}', '{pwd}')")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    pass
