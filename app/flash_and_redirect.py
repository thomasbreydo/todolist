from flask import Markup
from flask import flash


def flash_empty_input_and_redirect_to(message, redirect_func):
    flash(message)
    return redirect_func()


def flash_account_exists_and_redirect_to(redirect_func):
    flash(Markup(
        'An account with that email already exists. Login <a href="/login">here</a>.'))
    return redirect_func()


def flash_account_doesnt_exist_and_redirect_to(redirect_func):
    flash(Markup('An account with that email doesn\'t exist. Register '
                 '<a href="/register">here</a>.'))
    return redirect_func()


def flash_incorrect_password_and_redirect_to(redirect_func):
    flash("Incorrect password.")
    return redirect_func()
