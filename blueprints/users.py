from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from forms import LoginForm, RegisterForm
from databases import User, db


user = Blueprint('user', __name__)


@user.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.email.password

        user = User.query.filter(User.email == email).first()

        if not user:
            flash("There is no such user! You can register a new user!")
            return redirect(url_for("users.register"))
        elif password != user.password:
            flash("Wrong password!")
            return redirect(url_for("users.login"))
        else:
            login_user(user)
            flash("Login successfull!")
            return redirect(url_for("main.index"))

    return render_template('login.html')


@user.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User.query.filter(User.email == email).first()

        if user:
            flash("User already exists!")
            return redirect(url_for("users.register"))
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("User created successfully!")
            return redirect(url_for("users.login"))
