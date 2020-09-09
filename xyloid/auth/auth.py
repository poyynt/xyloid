from flask import Blueprint, flash, session, render_template, request, url_for, redirect
from passlib.hash import argon2
from ..db import db

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

def create_user(username, password):
    user = Users(username = username, password_hash = argon2.hash(password))
    db.session.add(user)
    db.session.commit()
    return username

def authenticate(username, password):
    user = Users.query.filter_by(username = username).first()
    if user is None:
        return False
    username = user.username
    password_hash = user.password_hash
    return argon2.verify(password, password_hash)

@auth.route("/login")
def login_page():
    if not session.get("logged_in"):
        return render_template("login.html")
    return redirect(url_for("admin.index"))

@auth.route("/login", methods=["POST"])
def login_verify():
    username, password = request.form.get("username"), request.form.get("password")
    redirect_to = request.form.get("redirect_to")
    if username is None or password is None:
        flash("Username or password cannot be empty")
        return redirect(url_for(".login_page"))
    if not authenticate(username, password):
        flash("Username or password is wrong")
        return redirect(url_for(".login_page"))
    session["logged_in"] = True
    session["username"] = username
    if redirect_to is None:
        return redirect(url_for("admin.index"))
    return redirect(redirect_to)

@auth.route("/logout")
def logout():
    session["logged_in"] = False
    session["username"] = None
    if request.headers.get("Referrer") is None:
        return redirect(url_for(".login_page"))
    return redirect(request.headers.get("Referrer"))

@auth.route("/change_password")
def change_password_page():
    if not session.get("logged_in"):
        flash("not logged in")
        return redirect(url_for(".login_page"))
    return render_template("reset_password.html")

@auth.route("/change_password", methods=["POST"])
def change_password():
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    new_password_repeat = request.form.get("new_password_repeat")
    if new_password != new_password_repeat:
        flash("passwords do not match")
        return redirect(url_for(".change_password_page"))
    if not authenticate(session["username"], old_password):
        flash("wrong password")
        return redirect(url_for(".change_password_page"))
    user = Users.query.filter_by(username = session["username"]).first()
    user.password_hash = argon2.hash(new_password)
    db.session.commit()
    return render_template("password_change_success.html")
