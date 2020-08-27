from flask import Markup
from flask import flash, session
import bcrypt


def extract_email_and_password(request):
    return request.form['email'], request.form['password']


def extract_name_email_and_password(request):
    return (request.form['name'],) + extract_email_and_password(request)


def empty_input(*fields):
    for field in fields:
        if len(field) == 0:
            return True
    return False


def flash_empty_input_and_redirect_to(redirect_func):
    flash("You must enter a username and password.")
    return redirect_func()


def flash_account_exists_and_redirect_to(redirect_func):
    flash(Markup('Your account already exists. Login <a href="/login">here</a>.'))
    return redirect_func()


def flash_account_doesnt_exist_and_redirect_to(redirect_func):
    flash(Markup('Your account doesn\'t exist. Register <a href="/register">here</a>.'))
    return redirect_func()


def logged_in():
    return "userId" in session


def get_current_user_id():
    return session["userId"]
