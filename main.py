#!/usr/bin/env python3
# coding: utf-8

import os.path
import sys

import flask

import data

FLASK_APP_PREFIX = ""
flask_app = flask.Flask(__name__)

flask_app.jinja_env.trim_blocks = True
flask_app.jinja_env.lstrip_blocks = True
flask_app.jinja_env.keep_trailing_newline = False

if (not os.path.exists("templates")):
	print("Should run from root folder")
	sys.exit()

@flask_app.route(FLASK_APP_PREFIX + "/")
def redirect_root():
	return flask.redirect("/index.html")


@flask_app.route(FLASK_APP_PREFIX + "/index.html")
def root():
	return flask.render_template("index.html", paragraphs=data.paragraphs)


@flask_app.route(FLASK_APP_PREFIX + "/blog.html")
def blog():
	return flask.render_template("blog.html", images_blog=data.images_blog)


@flask_app.route(FLASK_APP_PREFIX + "/my.html")
def my():
	return flask.render_template("my.html",
		images_impression=data.images_impression,
		images_march=data.images_march,
		images_photop=data.images_photop,
		images_other=data.images_other
	)


@flask_app.route(FLASK_APP_PREFIX + "/celtic.html")
def celtic():
	return flask.render_template("celtic.html", programs=data.programs)


#rss feeds
@flask_app.route(FLASK_APP_PREFIX + "/rss/paragraphs.xml")
def paragraphs_rss():
	return flask.render_template("rss/paragraphs.xml", paragraphs=reversed(data.paragraphs))


@flask_app.route(FLASK_APP_PREFIX + "/rss/celtic.xml")
def celtic_rss():
	return flask.render_template("rss/celtic.xml", programs=reversed(data.programs))

#numbered content
@flask_app.route(FLASK_APP_PREFIX + "/paragraphs/<string:index>.html")
def paragraph_text(index):
	try:
		index_int=int(index)
	except ValueError:
		flask.abort(400)

	if (os.path.isfile("templates/paragraphs/" + index + ".html") and index_int < len(data.paragraphs)):
		return flask.render_template(
			"paragraph_text.html",
			index_int=index_int,
			paragraphs=data.paragraphs
		)
	else:
		flask.abort(404)


@flask_app.route(FLASK_APP_PREFIX + "/celtic/<string:index>.html")
def celtic_text(index):
	try:
		index_int=int(index)
	except ValueError:
		flask.abort(400)

	if (os.path.isfile("templates/celtic/" + index + ".html") and index_int <= len(data.programs)):
		return flask.render_template(
			"celtic_text.html",
			index_int=index_int,
			programs=data.programs
		)
	else:
		flask.abort(404)


@flask_app.route(FLASK_APP_PREFIX + "/<path:filename>")
def everything_else(filename):
	if os.path.isfile(os.path.join("templates/static", filename)):
		return flask.render_template("static/" + filename)
	elif os.path.isfile(os.path.join("static", filename)):
		return flask_app.send_static_file(filename)
	else:
		flask.abort(http.client.NOT_FOUND, flask.request.base_url)


#setting error handlers
@flask_app.errorhandler(404)
def http_not_found(error):
	return (flask.render_template("404.html"), 404)


@flask_app.errorhandler(403)
def http_forbidden(error):
	return (flask.render_template("403.html"), 403)


@flask_app.errorhandler(400)
def http_bad_request(error):
	return (flask.render_template("400.html"), 400)

if __name__ == "__main__":
	flask_app.run(host="0.0.0.0")

app = flask_app
