### xyloid

Xyloid is a simple personal blog written in python with flask. 

#### Installation
First, clone this repository.
Then install the requirements:
`python3 -m pip install -r requirements.txt`
Set up a webserver, and set up the database.


The database structure must be like this:


Main database:


```
|--- post_content
|    |--- post_id			INTEGER NOT NULL UNIQUE PRIMARY KEY
|    |--- content			TEXT NOT NULL
|--- posts
|    |--- internal_id			INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL
|    |--- name				VARCHAR(256) NOT NULL
|    |--- shortlink			VARCHAR(16) UNIQUE
|    |--- uuid				VARCHAR(36) UNIQUE NOT NULL
|    |--- created			DATE NOT NULL
|--- users
|    |--- user_id			INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL
|    |--- username			VARCHAR(32) UNIQUE NOT NULL
|    |--- password_hash			VARCHAR(128) NOT NULL
```

A SQL Schema file is provided for creating the database.

Make a random secret key for the app (16 bytes is ok) and write it in `xyloid/secret_key`.

Then create users like this (passwords are hashed using argon2):
```
$ python3
>>> from xyloid.auth.auth import create_user
>>> from xyloid.app import app
>>> with app.test_request_context():
...     create_user("your username", "your password")
```
And finally set up the blog name (shown in page titles) in `config.py` to your desired name.

#### TODO
- [ ] Make the admin panel useful (you can only post by entering the URL /admin/new into your browser's address bar after logging in).
- [ ] Make the whole thing more pretty.
- [ ] Add edit functionality.
- [ ] Write template files for resetting and changing password.

