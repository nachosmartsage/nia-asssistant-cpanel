from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from apps.__init__ import get_db
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = get_db().users.find_one({"username": username})

        # Check the password
        if user and verify_pass(password, user['password']):
            login_user(user)
            return redirect(url_for('home_blueprint.index'))

    return render_template('accounts/login.html', form=login_form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    register_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        # Extract form data
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if get_db().users.find_one({"username": username}):
            return render_template('accounts/register.html', form=register_form, error="User already exists!")

        # If user does not exist, create a new one
        get_db().users.insert_one({"username": username, "password": password})
        return redirect(url_for('authentication_blueprint.login'))

    return render_template('accounts/register.html', form=register_form)
