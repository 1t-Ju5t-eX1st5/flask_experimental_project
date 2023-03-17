from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .passwords import check_password
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('User does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email is already in use', category='error')
        elif len(email) < 4:
            flash('Email must be longer than 4 characters', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character', category='error')
        else:
            res = check_password(password1, password2)
            if res:
                flash(res, category='error')
            else:
                # add user to the database
                new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'), created_date=datetime.now())
                db.session.add(new_user)
                db.session.commit()
                # login_user(user) --- original code
                login_user(new_user) # correct code
                flash('Account created successfully!', category='success')
                return redirect(url_for('views.home'))

    elif request.method == "GET":
        pass
    else:
        pass

    return render_template("signup.html", user=current_user)

@auth.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == "POST":
        current_password = request.form.get('current-password')
        new_password = request.form.get('new-password')
        confirm_new_password = request.form.get('confim-password')
        if not check_password_hash(current_user.password, current_password):
                flash('Current password does not match', category='error')
        elif new_password == current_password:
            flash('New password cannot be same as old password', category='error')
        elif new_password == confirm_new_password:
            flash('Passwords do not match', category='error')
        else:
            res = check_password(new_password)
            if res:
                flash(res, category='error')
            else:
                current_user.reset_password(new_password)
                db.session.commit()
                return redirect(url_for('views.home'))
    elif request.method == 'GET':
        pass
    else:
        pass

    return render_template('reset_password.html')