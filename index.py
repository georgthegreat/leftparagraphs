#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from data import *
import os.path

theApp = Flask(__name__)
theApp.debug = True

@theApp.route("/")
def root():
	return render_template("index.html", paragraphs=paragraphs)

@theApp.route("/index.html")
def anotherRoot():
	return render_template("index.html", paragraphs=paragraphs)

@theApp.route("/blog.html")
def blog():
	return render_template("blog.html", blogImages=blogImages)

@theApp.route("/my.html")
def my():
	return render_template("my.html", impressionImages=impressionImages, marchImages=marchImages, photopImages=photopImages, drugoeImages=drugoeImages)

@theApp.route("/celtic.html")
def celtic():
	return render_template("celtic.html", programs=programs)

@theApp.route("/about.html")
def about():
	return render_template("about.html")

#rss feeds
@theApp.route("/rss/paragraphs.xml")
def paragraphs_rss():
	return render_template("rss/paragraphs.xml", paragraphs=reversed(paragraphs))

@theApp.route("/rss/celtic.xml")
def celtic_rss():
	return render_template("rss/celtic.xml", programs=reversed(programs)	)

#numbered content
@theApp.route("/paragraphs/<string:index>.html")
def paragraph_text(index):
	if (os.path.isfile("templates/paragraphs/" + number)):
		return render_template("404.html"), 200
	else:
		return render_template("404.html"), 404

@theApp.route("/celtic/<string:index>.html")
def celtic_text(index):
	if (os.path.isfile("templates/celtic/" + index + ".html")):
		return render_template("celtic_text.html", intIndex=int(index), programs=programs)
	else:
		return render_template("404.html"), 404

#static content
@theApp.route("/other/<path:filename>")
def other(filename):
	return render_template("other/" + filename)

@theApp.route("/<string:subfolder>/<path:filename>")
def static(subfolder, filename):
	return theApp.send_static_file(subfolder + "/" + filename)

@theApp.route("/robots.txt")
def robots():
	return theApp.send_static_file("robots.txt")

#setting error handlers
@theApp.errorhandler(404)
def http_not_found(error):
	return render_template("404.html"), 404

@theApp.errorhandler(403)
def http_not_found(error):
	return render_template("403.html"), 403

if __name__ == "__main__":
	theApp.run(host="0.0.0.0")

