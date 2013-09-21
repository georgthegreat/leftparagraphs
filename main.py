#!/usr/bin/env python3
# coding: utf-8

import os.path
import sys

from flask import Flask, render_template, abort, redirect

import data

APP_PREFIX = ""

app = Flask(__name__)

app.jinja_env.trim_blocks = True

if (not os.path.exists("templates")):
	print("Should run from root folder")
	sys.exit()

@app.route(APP_PREFIX + "/")
def redirect_root():
	return redirect("/index.html")


@app.route(APP_PREFIX + "/index.html")
def root():
	return render_template("index.html", paragraphs=data.paragraphs)


@app.route(APP_PREFIX + "/blog.html")
def blog():
	return render_template("blog.html", images_blog=data.images_blog)


@app.route(APP_PREFIX + "/my.html")
def my():
	return render_template("my.html",
		images_impression=data.images_impression,
		images_march=data.images_march,
		images_photop=data.images_photop,
		images_other=data.images_other
	)


@app.route(APP_PREFIX + "/celtic.html")
def celtic():
	return render_template("celtic.html", programs=data.programs)


#rss feeds
@app.route(APP_PREFIX + "/rss/paragraphs.xml")
def paragraphs_rss():
	return render_template("rss/paragraphs.xml", paragraphs=reversed(data.paragraphs))


@app.route(APP_PREFIX + "/rss/celtic.xml")
def celtic_rss():
	return render_template("rss/celtic.xml", programs=reversed(data.programs))

#numbered content
@app.route(APP_PREFIX + "/paragraphs/<string:index>.html")
def paragraph_text(index):
	try:
		index_int=int(index)
	except ValueError:
		abort(400)

	if (os.path.isfile("templates/paragraphs/" + index + ".html") and index_int < len(data.paragraphs)):
		return render_template(
			"paragraph_text.html",
			index_int=index_int,
			paragraphs=data.paragraphs
		)
	else:
		abort(404)


@app.route(APP_PREFIX + "/celtic/<string:index>.html")
def celtic_text(index):
	try:
		index_int=int(index)
	except ValueError:
		abort(400)

	if (os.path.isfile("templates/celtic/" + index + ".html") and index_int <= len(data.programs)):
		return render_template(
			"celtic_text.html",
			index_int=index_int,
			programs=data.programs
		)
	else:
		abort(404)


@app.route(APP_PREFIX + "/<path:filename>")
def everything_else(filename):
	if (os.path.isfile("templates/" + filename)):
		return render_template(filename)
	elif (os.path.isfile("static/" + filename)):
		return app.send_static_file(filename)
	else:
		abort(404)


#setting error handlers
@app.errorhandler(404)
def http_not_found(error):
	return (render_template("404.html"), 404)


@app.errorhandler(403)
def http_forbidden(error):
	return (render_template("403.html"), 403)


@app.errorhandler(400)
def http_forbidden(error):
	return (render_template("400.html"), 400)

if __name__ == "__main__":
	app.run(host="0.0.0.0")

