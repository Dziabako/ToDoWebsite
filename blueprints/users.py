from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, LoginManager
from blueprints.forms import LoginForm, RegisterForm
from blueprints.databases import User, db
from werkzeug.security import generate_password_hash, check_password_hash


user = Blueprint('user', __name__)


login_manager = LoginManager()
login_manager.login_view = 'user.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


@user.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter(User.email == email).first()

        if not user:
            flash("There is no such user! You can register a new user!")
            return redirect(url_for("user.register"))
        elif not check_password_hash(user.password, password):
            flash("Wrong password!")
            return redirect(url_for("user.login"))
        else:
            login_user(user)
            flash("Login successful!")
            return redirect(url_for("todo.todos", user_id=user.id))

    return render_template('login.html', form=form)


@user.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)


        user = User.query.filter(User.email == email).first()

        if user:
            flash("User already exists!")
            return redirect(url_for("user.register"))
        else:
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("User created successfully!")
            return redirect(url_for("user.login"))
    
    return render_template("register.html", form=form)
        

@user.route("/logout")
def logout():
    logout_user()
    flash("Logout successful!")
    return redirect(url_for("main.index"))
