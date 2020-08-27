import sqlite3
from contextlib import contextmanager
from flask import session
import bcrypt
from .auth import get_current_user_id

DB = sqlite3.connect("database.db", check_same_thread=False)


@contextmanager
def cursor(connection):
    c = connection.cursor()
    try:
        yield c
    finally:
        connection.commit()
        c.close()


def get_current_user_row():
    with cursor(DB) as c:
        c.execute("SELECT * FROM users WHERE id = ?", [get_current_user_id()])
        return c.fetchone()


def get_current_user_name():
    return get_current_user_row()[1]


def add_user(name, email, password):
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())  # !
    with cursor(DB) as c:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", [
                  name, email, hashed])


def account_exists(email):
    row = get_user_row_from_email(email)
    return row is not None


def get_user_row_from_email(email):
    c = DB.cursor()
    c.execute("SELECT id FROM users WHERE email = ?", [email])
    row = c.fetchone()
    c.close()
    return row


def get_user_id_from_email(email):
    return get_user_row_from_email(email)[0]
