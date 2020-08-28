from flask import session


def logged_in():
    return "userId" in session


def get_current_user_id():
    return session["userId"]


def set_current_user_by_email(email):
    from .database import get_user_id_from_email  # noqa
    session["userId"] = get_user_id_from_email(email)
