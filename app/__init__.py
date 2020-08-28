from flask import Flask
from flask import session, redirect, render_template, request
from .utils import empty_input
from .redirect import flash_account_exists_and_redirect_to
from .redirect import flash_account_doesnt_exist_and_redirect_to
from .redirect import flash_empty_input_and_redirect_to
from .database import get_user_row_from_email
from .database import account_exists
from .database import add_user
from .database import get_current_user_row
from .database import get_current_user_name
from .database import get_user_id_from_email
from .database import check_password
from .manage_requests import extract_email_and_password
from .manage_requests import extract_name_email_and_password
from .secrets import SECRET_KEY
from .state import logged_in
from .state import set_current_user_by_email

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/")
def index():
    if logged_in():
        return redirect("/home")
    return render_template("login.html")


@app.route("/register", methods=["GET"])
def register_page():
    if logged_in():
        return redirect("/home")
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    name, email, password = extract_name_email_and_password(request)
    if empty_input(name, email, password):
        return flash_empty_input_and_redirect_to(register_page)
    if account_exists(email):
        return flash_account_exists_and_redirect_to(register_page)
    add_user(name, email, password)
    set_current_user_by_email(email)
    return index()


@app.route("/logout", methods=["POST"])
def logout():
    del session["userId"]
    return index()


@app.route("/logout", methods=["GET"])
def logout_page():
    if logged_in():
        return render_template("logout.html")
    return login_page()


@app.route("/login", methods=["POST"])
def login():
    email, password = extract_email_and_password(request)
    if empty_input(email, password):
        return flash_empty_input_and_redirect_to(login_page)
    if not account_exists(email):
        return flash_account_doesnt_exist_and_redirect_to(login_page)
    if check_password(email, password):
        set_current_user_by_email(email)
        return home_page()
        # check password


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/home", methods=["GET"])
def home_page():
    if logged_in():
        return render_template("home.html", name=get_current_user_name())
    return login_page()
