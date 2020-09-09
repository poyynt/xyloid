from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from ..config import config

post = Blueprint("post", __name__, static_folder="static", template_folder="templates")

@post.route("/<shortlink>")
def by_shortlink(shortlink):
	return render_template("post.html", shortlink = shortlink, uuid = None, blog=config["blog_name"])

@post.route("/uuid/<uuid>")
def by_uuid(uuid):
	return render_template("post.html", shortlink = None, uuid = uuid, blog=config["blog_name"])
