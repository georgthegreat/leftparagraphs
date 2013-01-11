#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from data import *
import os.path
import sys

import logging
from logging import Formatter

theApp = Flask(__name__)
theApp.debug = True
theApp.jinja_env.trim_blocks = True

if (not os.path.exists(u"templates")):
	print(u"Should run from root folder")
	sys.exit()

@theApp.route(u"/")
def root():
	return render_template(u"index.html", paragraphs=paragraphs)

@theApp.route(u"/index.html")
def anotherRoot():
	return render_template(u"index.html", paragraphs=paragraphs)

@theApp.route(u"/blog.html")
def blog():
	return render_template(u"blog.html", blogImages=blogImages)

@theApp.route(u"/my.html")
def my():
	return render_template(u"my.html", impressionImages=impressionImages, marchImages=marchImages, photopImages=photopImages, drugoeImages=drugoeImages)

@theApp.route(u"/celtic.html")
def celtic():
	return render_template(u"celtic.html", programs=programs)

@theApp.route(u"/about.html")
def about():
	return render_template(u"about.html")

#rss feeds
@theApp.route(u"/rss/paragraphs.xml")
def paragraphs_rss():
	return render_template(u"rss/paragraphs.xml", paragraphs=reversed(paragraphs))

@theApp.route(u"/rss/celtic.xml")
def celtic_rss():
	return render_template(u"rss/celtic.xml", programs=reversed(programs)	)

#numbered content
@theApp.route(u"/paragraphs/<string:index>.html")
def paragraph_text(index):
	try:
		intIndex=int(index)
	except ValueError:
		return http_not_found(404)

	if (os.path.isfile(u"templates/paragraphs/" + index + u".html") and intIndex < len(paragraphs)):
		return render_template(u"paragraph_text.html", intIndex=intIndex, paragraphs=paragraphs)
	else:
		return http_not_found(404)

@theApp.route(u"/celtic/<string:index>.html")
def celtic_text(index):
	try:
		intIndex=int(index)
	except ValueError:
		return http_not_found(404)

	if (os.path.isfile(u"templates/celtic/" + index + u".html") and intIndex <= len(programs)):
		return render_template(u"celtic_text.html", intIndex=int(index), programs=programs)
	else:
		return http_not_found(404)

#static content
@theApp.route(u"/other/<path:filename>")
def other(filename):
	return render_template(u"other/" + filename)

@theApp.route(u"/<path:filename>")
def static(filename):
	if (os.path.isfile(u"static/" + filename)):
		return theApp.send_static_file(filename)
	
#setting error handlers
@theApp.errorhandler(404)
def http_not_found(error):
	theApp.logger.error(u"Error #404 occured")
	return render_template(u"404.html"), 404

@theApp.errorhandler(403)
def http_forbidden(error):
	theApp.logger.error(u"Error #403 occured")
	return render_template(u"403.html"), 403

file_handler = logging.FileHandler(u"leftparagraphs.log", mode=u"a", encoding=None, delay=False)
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

