from flask import Blueprint, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from ..db import db
from .. import utils
import datetime
from uuid import uuid4
from sqlalchemy import func, desc

api = Blueprint("api", __name__)

class Posts(db.Model):
	internal_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
	name = db.Column(db.String(256), nullable=False)
	shortlink = db.Column(db.String(16), unique=True)
	uuid = db.Column(db.String(36), unique=True, nullable=False)
	created = db.Column(db.DateTime, nullable=False)
	category1 = db.Column(db.String(32))
	category2 = db.Column(db.String(32))
	category3 = db.Column(db.String(32))
	category4 = db.Column(db.String(32))
	category5 = db.Column(db.String(32))

class PostContent(db.Model):
	post_id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
	content = db.Column(db.Text, nullable=False)

@api.route("/posts/all")
@api.route("/posts/all/<int:page>")
def all_posts(page = 1):
	result = list(Posts.query.order_by(desc(Posts.internal_id)).paginate(page = page, per_page=20, max_per_page=20).items)
	result = [{"name": r.name, "uuid": r.uuid, "shortlink": r.shortlink, "created": r.created, "categories": [r.category1, r.category2, r.category3, r.category4, r.category5]} for r in result]
	return jsonify(result)

@api.route("/posts/count/all")
def posts_count():
	return str(Posts.query.count())

@api.route("/posts/info/<uuid>")
def get_post_info(uuid):
	result = Posts.query.filter_by(uuid = uuid).first()
	if result is None:
		return jsonify({"error": "uuid not found"}), 404
	return jsonify({"name": result.name, "shortlink": result.shortlink, "uuid": result.uuid, "created": result.created, "categories": [result.category1, result.category2, result.category3, result.category4, result.category5]})

@api.route("/posts/info/by_shortlink/<shortlink>")
def get_post_info_by_shortlink(shortlink):
	result = Posts.query.filter_by(shortlink = shortlink).first()
	if result is None:
		return jsonify({"error": "shortlink not found"}), 404
	return jsonify({"name": result.name, "shortlink": result.shortlink, "uuid": result.uuid, "created": result.created, "categories": [result.category1, result.category2, result.category3, result.category4, result.category5]})

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
	categories = [request.json.get(f"category{i}").lower() for i in range(1, 6)]
	if name == "" or content.strip() == "":
		return jsonify({"error": "name or content cannot be empty"}), 400
	uuid = str(uuid4())
	info = Posts(name=name, shortlink=shortlink, uuid=uuid, created=datetime.datetime.now(datetime.timezone.utc), category1=categories[0], category2=categories[1], category3=categories[2], category4=categories[3], category5=categories[4])
	db.session.add(info)
	db.session.commit()
	post_content = PostContent(post_id = info.internal_id, content = content)
	db.session.add(post_content)
	db.session.commit()
	return jsonify({"uuid": uuid, "shortlink": shortlink})

@api.route("/posts/delete/<uuid>")
def delete_post(uuid):
	if not session.get("logged_in"):
		return jsonify({"error": "not logged in"}), 401
	post = Posts.query.filter_by(uuid = uuid).first()
	post_content = PostContent.query.filter_by(post_id = post.internal_id).first()
	db.session.delete(post_content)
	db.session.delete(post)
	db.session.commit()
	return jsonify({"status": "success", "uuid": uuid})

@api.route("/posts/edit/<uuid>", methods=["POST"])
def edit_post(uuid):
	if not session.get("logged_in"):
		return jsonify({"error": "not logged in"}), 401
	post = Posts.query.filter_by(uuid = uuid).first()
	name = request.json.get("name")
	content = request.json.get("content")
	categories = [request.json.get(f"category{i}").lower() for i in range(1, 6)]
	if name is None or content is None:
		return jsonify({"error": "name or content cannot be empty"}), 400
	post.name = name
	post.created = datetime.datetime.now(datetime.timezone.utc)
	post.category1 = categories[0]
	post.category2 = categories[1]
	post.category3 = categories[2]
	post.category4 = categories[3]
	post.category5 = categories[4]
	post_content = PostContent.query.filter_by(post_id = post.internal_id).first()
	post_content.content = content
	db.session.commit()
	return jsonify({"status": "success", "uuid": uuid})

@api.route("/posts/<category>")
@api.route("/posts/<category>/<int:page>")
def posts_by_category(category, page = 1):
	category = category.lower()
	if category not in ("uncategorized"):
		result = list(Posts.query.filter((Posts.category1 == category) | (Posts.category2 == category) | (Posts.category3 == category) | (Posts.category4 == category) | (Posts.category5 == category)).order_by(desc(Posts.internal_id)).paginate(page=page, per_page=20, max_per_page=20).items)
	else:
		result = list(Posts.query.filter_by(category1="", category2="", category3="", category4="", category5="").order_by(desc(Posts.internal_id)).paginate(page=page, per_page=20, max_per_page=20).items)
	result = [{"uuid": r.uuid} for r in result]
	return jsonify(result)
@api.route("/posts/count/<category>")
def category_count(category):
	if category not in ("uncategorized"):
		result = Posts.query.filter((Posts.category1 == category) | (Posts.category2 == category) | (Posts.category3 == category) | (Posts.category4 == category) | (Posts.category5 == category)).count()
	else:
		result = Posts.query.filter_by(category1="", category2="", category3="", category4="", category5="").count()
	return str(result)

@api.route("/categories")
def get_categories():
	result = Posts.query.with_entities(Posts.category1).union_all(Posts.query.with_entities(Posts.category2)).union_all(Posts.query.with_entities(Posts.category3)).union_all(Posts.query.with_entities(Posts.category4)).union_all(Posts.query.with_entities(Posts.category5)).filter(Posts.category1 != "").group_by(Posts.category1).with_entities(Posts.category1, func.count(Posts.category1)).order_by(desc(func.count(Posts.category1))).all()
	uncategorized = Posts.query.filter((Posts.category1 == "") & (Posts.category2 == "") & (Posts.category3 == "") & (Posts.category4 == "") & (Posts.category5 == "")).count()
	result += [("uncategorized", uncategorized), ("all", Posts.query.count())]
	result = [{"name": r[0], "count": r[1]} for r in result]
	return jsonify(result)
