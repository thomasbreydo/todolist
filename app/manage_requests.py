from flask import request


def extract_email_and_password(request):
    return request.form['email'], request.form['password']


def extract_name_email_and_password(request):
    return (request.form['name'],) + extract_email_and_password(request)


def empty_input(*fields):
    for field in fields:
        if len(field) == 0:
            return True
    return False
