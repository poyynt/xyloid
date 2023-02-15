import os

config = {
	"blog_name": os.environ.get("XYLOID_BLOG_NAME", default="Blog"),
	"minify": True,
}
