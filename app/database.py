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


@contextmanager
def isolation_level_none_cursor(connection):
    old = connection.isolation_level
    try:
        connection.isolation_level = None
        with cursor(connection) as c:
            yield c
    finally:
        connection.isolation_level = old


def get_current_user_row():
    with cursor(DB_CONNECTION) as c:
        c.execute("SELECT * FROM users WHERE id = ?;", [get_current_user_id()])
        return c.fetchone()


def get_current_user_name():
    return get_current_user_row()[1]


def add_user(name, email, password):
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())  # !
    with cursor(DB_CONNECTION) as c:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?);", [
                  name, email, hashed])


def account_exists(email):
    row = get_user_row_from_email(email)
    return row is not None


def get_user_row_from_email(email):
    c = DB_CONNECTION.cursor()
    c.execute("SELECT * FROM users WHERE email = ?;", [email])
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
    with isolation_level_none_cursor(DB_CONNECTION) as c:
        c.execute("DELETE FROM users;")
        c.execute("VACUUM;")


def reset_todos():
    with isolation_level_none_cursor(DB_CONNECTION) as c:
        c.execute("DELETE FROM todos;")
        c.execute("VACUUM;")


def reset_database():
    reset_users()
    reset_todos()


def new_todo(content):
    userId = get_current_user_id()
    with cursor(DB_CONNECTION) as c:
        c.execute("INSERT INTO todos (userId, done, content) VALUES (?, 0, ?);",
                  [userId, content])


def delete_todo(todoId):
    with cursor(DB_CONNECTION) as c:
        c.execute("DELETE FROM todos WHERE id = ?", [todoId])


def mark_todo_done(todoId):
    with cursor(DB_CONNECTION) as c:
        c.execute("UPDATE todos SET done = 1 WHERE id = ?", [todoId])


def toggle_todo(todoId):
    with cursor(DB_CONNECTION) as c:
        c.execute("UPDATE todos SET done = (1 - done) WHERE id = ?", [todoId])


def get_todos():
    userId = get_current_user_id()
    with cursor(DB_CONNECTION) as c:
        c.execute("SELECT * FROM todos WHERE userId = ?", [userId])
        return c.fetchall()
