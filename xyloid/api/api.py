from flask import Blueprint, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from ..db import db
from .. import utils
import datetime
from uuid import uuid4

api = Blueprint("api", __name__)

class Posts(db.Model):
	internal_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
	name = db.Column(db.String(256), nullable=False)
	shortlink = db.Column(db.String(16), unique=True)
	uuid = db.Column(db.String(36), unique=True, nullable=False)
	created = db.Column(db.DateTime, nullable=False)

class PostContent(db.Model):
	post_id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
	content = db.Column(db.Text, nullable=False)

@api.route("/posts/all")
@api.route("/posts/all/<int:page>")
def all_posts(page = 1):
	result = list(Posts.query.paginate(page = page, per_page=20, max_per_page=20).items)
	result = [{"name": r.name, "uuid": r.uuid, "shortlink": r.shortlink, "created": r.created} for r in result]
	return jsonify(result)

@api.route("/posts/info/<uuid>")
def get_post_info(uuid):
	result = Posts.query.filter_by(uuid = uuid).first()
	if result is None:
		return jsonify({"error": "uuid not found"}), 404
	return jsonify({"name": result.name, "shortlink": result.shortlink, "uuid": result.uuid, "created": result.created})

@api.route("/posts/info/by_shortlink/<shortlink>")
def get_post_info_by_shortlink(shortlink):
	result = Posts.query.filter_by(shortlink = shortlink).first()
	if result is None:
		return jsonify({"error": "shortlink not found"}), 404
	return jsonify({"name": result.name, "shortlink": result.shortlink, "uuid": result.uuid, "created": result.created})

@api.route("/posts/content/<uuid>")
def get_post_content(uuid):
	try:
		post_id = Posts.query.filter_by(uuid = uuid).first().internal_id
	except AttributeError:
		return jsonify({"error": "uuid not found"}), 404
	result = PostContent.query.filter_by(post_id = post_id).first().content
	return jsonify({"uuid": uuid, "content": result})

@api.route("/posts/create", methods=["POST"])
def create_post():
	if not session.get("logged_in"):
		return jsonify({"error": "not logged in"}), 401
	name = request.json.get("name")
	shortlink = utils.create_shortlink()
	content = request.json.get("content")
	if name == "" or content.strip() == "":
		return jsonify({"error": "name or content cannot be empty"}), 400
	uuid = str(uuid4())
	info = Posts(name = name, shortlink = shortlink, uuid = uuid, created = datetime.datetime.now(datetime.timezone.utc))
	db.session.add(info)
	db.session.commit()
	post_content = PostContent(post_id = info.internal_id, content = content)
	db.session.add(post_content)
	db.session.commit()
	return jsonify({"uuid": uuid, "shortlink": shortlink})
