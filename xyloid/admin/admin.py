from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from ..db import db

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route("/")
def index():
	if not session.get("logged_in"):
		flash("Not logged in")
		return redirect(url_for("auth.login_page"))
	return render_template("index.html")

@admin.route("/new")
def new():
	if not session.get("logged_in"):
		flash("Not logged in")
		return redirect(url_for("auth.login_page"))
	return render_template("new.html")

@admin.route("/posts")
def posts():
	if not session.get("logged_in"):
		flash("Not logged in")
		return redirect(url_for("auth.login_page"))
	return render_template("posts.html")

@admin.route("/edit/<uuid>")
def edit(uuid):
	if not session.get("logged_in"):
		flash("Not logged in")
		return redirect(url_for("auth.login_page"))
	return render_template("edit.html", uuid = uuid)
