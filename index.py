#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import abort

import data

import os.path
import sys

import logging
from logging import Formatter

theApp = Flask(__name__)
theApp.debug = True
theApp.jinja_env.trim_blocks = True

if (not os.path.exists("templates")):
	print("Should run from root folder")
	sys.exit()

@theApp.route("/")
def root():
	return render_template("index.html", paragraphs=data.paragraphs)


@theApp.route("/index.html")
def anotherRoot():
	return render_template("index.html", paragraphs=data.paragraphs)


@theApp.route("/blog.html")
def blog():
	return render_template("blog.html", images_blog=data.images_blog)


@theApp.route("/my.html")
def my():
	return render_template("my.html", images_impression=data.images_impression, images_march=data.images_march, images_photop=data.images_photop, images_other=images_other)


@theApp.route("/celtic.html")
def celtic():
	return render_template("celtic.html", programs=data.programs)


#rss feeds
@theApp.route("/rss/paragraphs.xml")
def paragraphs_rss():
	return render_template("rss/paragraphs.xml", paragraphs=reversed(data.paragraphs))


@theApp.route("/rss/celtic.xml")
def celtic_rss():
	return render_template("rss/celtic.xml", programs=reversed(data.programs))

#numbered content
@theApp.route("/paragraphs/<string:index>.html")
def paragraph_text(index):
	try:
		int_index=int(index)
	except ValueError:
		abort(400)

	if (os.path.isfile("templates/paragraphs/" + index + ".html") and int_index < len(data.paragraphs)):
		return render_template("paragraph_text.html", int_index=int_index, paragraphs=data.paragraphs)
	else:
		abort(404)


@theApp.route("/celtic/<string:index>.html")
def celtic_text(index):
	try:
		int_index=int(index)
	except ValueError:
		abort(400)

	if (os.path.isfile("templates/celtic/" + index + ".html") and int_index <= len(data.programs)):
		return render_template("celtic_text.html", int_index=int(index), programs=data.programs)
	else:
		abort(404)


@theApp.route("/<path:filename>")
def everything_else(filename):
	if (os.path.isfile("templates/" + filename)):
		return render_template(filename)
	elif (os.path.isfile("static/" + filename)):
		return theApp.send_static_file(filename)
	else:
		abort(404)


#setting error handlers
@theApp.errorhandler(404)
def http_not_found(error):
	theApp.logger.error("Error #404 occured")
	return (render_template("404.html"), 404)


@theApp.errorhandler(403)
def http_forbidden(error):
	theApp.logger.error("Error #403 occured")
	return (render_template("403.html"), 403)


@theApp.errorhandler(400)
def http_forbidden(error):
	theApp.logger.error("Error #400 occured")
	return (render_template("400.html"), 400)


file_handler = logging.FileHandler("leftparagraphs.log", mode="a", encoding=None, delay=False)
file_handler.setFormatter(Formatter(
'''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Message: %(message)s

'''))
file_handler.setLevel(logging.WARNING)
theApp.logger.addHandler(file_handler)
	
if __name__ == "__main__":
	theApp.run(host="0.0.0.0")

