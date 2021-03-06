CREATE TABLE posts (internal_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, name VARCHAR (256) NOT NULL, shortlink VARCHAR (16) UNIQUE, uuid VARCHAR (36) UNIQUE NOT NULL, created DATE NOT NULL, category1 VARCHAR (32), category2 VARCHAR (32), category3 VARCHAR (32), category4 VARCHAR (32), category5 VARCHAR (32));
CREATE INDEX post_id_index ON posts (internal_id ASC);
CREATE TABLE post_content (post_id INTEGER NOT NULL UNIQUE PRIMARY KEY, content TEXT NOT NULL);
CREATE INDEX post_content_id_index ON post_content (post_id ASC);
CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, username VARCHAR(32) UNIQUE NOT NULL, password_hash VARCHAR(128) NOT NULL);
