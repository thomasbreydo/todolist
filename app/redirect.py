from flask import Markup
from flask import flash


def flash_empty_input_and_redirect_to(redirect_func):
    flash("You must enter a username and password.")
    return redirect_func()


def flash_account_exists_and_redirect_to(redirect_func):
    flash(Markup('Your account already exists. Login <a href="/login">here</a>.'))
    return redirect_func()


def flash_account_doesnt_exist_and_redirect_to(redirect_func):
    flash(Markup('Your account doesn\'t exist. Register <a href="/register">here</a>.'))
    return redirect_func()
