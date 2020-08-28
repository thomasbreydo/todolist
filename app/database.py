import sqlite3
from contextlib import contextmanager
from flask import session
import bcrypt
from .state import get_current_user_id
from .utils import asbytes


DB_CONNECTION = sqlite3.connect("database.db", check_same_thread=False)


@contextmanager
def cursor(connection):
    c = connection.cursor()
    try:
        yield c
    finally:
        connection.commit()
        c.close()


def get_current_user_row():
    with cursor(DB_CONNECTION) as c:
        c.execute("SELECT * FROM users WHERE id = ?", [get_current_user_id()])
        return c.fetchone()


def get_current_user_name():
    return get_current_user_row()[1]


def add_user(name, email, password):
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())  # !
    with cursor(DB_CONNECTION) as c:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", [
                  name, email, hashed])


def account_exists(email):
    row = get_user_row_from_email(email)
    return row is not None


def get_user_row_from_email(email):
    c = DB_CONNECTION.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", [email])
    row = c.fetchone()
    c.close()
    return row


def get_user_id_from_email(email):
    return get_user_row_from_email(email)[0]


def get_password_from_email(email):
    return get_user_row_from_email(email)[3]


def check_password(email, password):
    password_to_check = asbytes(password)
    true_password = asbytes(get_password_from_email(email))
    return bcrypt.checkpw(password_to_check, true_password)


def reset_users():
    with cursor(DB_CONNECTION) as c:
        c.execute("DROP TABLE users")
        c.execute(
            "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email "
            "TEXT, password TEXT)")
