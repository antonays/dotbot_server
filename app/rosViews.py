import os, json, sys, datetime
from flask import Blueprint
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app, connectedBot
from models import *
import requests

rosViews = Blueprint('rosViews', __name__)


@rosViews.route('/file/edit/<int:id>')
def edit_file(id):
	s = File.query.get_or_404(id)
	return render_template('ros/edit.html', file=s)

@rosViews.route('/nodes')
def nodes():
	return render_template('ros/nodes.html', current_time=datetime.utcnow())

@rosViews.route('/nodes/<int:id>')
def files_of_node(id):
	return render_template('ros/files.html', current_time=datetime.utcnow(), node_id = id)

@rosViews.route('/rosnodes')
def rosnodes():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	bot=None
	if (session.get('connectedBot')):
		print ("bot in session")
		try:
			if (app.connectedBot is not None):
				print ("bot exists")
				bot = app.connectedBot
		except AttributeError:
			print ("No Connected Bot in context - Server was reset?")
			bot=None
	return render_template('ros/rosnodes.html', current_time=datetime.utcnow(), bot=bot)

@rosViews.route('/rostopics')
def rostopics():
	return render_template('ros/rostopics.html', current_time=datetime.utcnow())

@rosViews.route('/rosconnect', methods=['GET','POST'])
def rosconnect():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	app.connectedBot = models.Bot(request.form["name"],request.form)
	print ("bot created")
	session["connectedBot"] = request.form["ip"]
	return render_template('ros/rosconsole.html', current_time=datetime.utcnow(), bot=app.connectedBot)	

@rosViews.route('/rosconsole', methods=['GET','POST'])
def rosconsole():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	bot=None
	if (session.get('connectedBot')):
		print ("bot in session")
		try:
			if (app.connectedBot is not None):
				print ("bot exists")
				bot = app.connectedBot
		except AttributeError:
			print ("No Connected Bot in context - Server was reset?")
			bot=None
	return render_template('ros/rosconsole.html', current_time=datetime.utcnow(), bot=bot)

@rosViews.route('/disc_rosconsole')
def disc_rosconsole():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	session["connectedBot"] = None
	connectedBot = None
	return render_template('ros/rosconsole.html', current_time=datetime.utcnow(), bot =None)	

@rosViews.route('/run_roscore', methods=['GET'])
def run_roscore():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	address = request.args.get("targetAdress")
	r = requests.get("http://"+address+":5000/roscore")
	if (r.status_code == 200):
		print ("core started")
		############TODO: notify all nodes about roscore started
	else:
		print ("core failed to start")
	return "ok"

@rosViews.route('/test')
def test_page():
	return render_template('ros/test.html')

@rosViews.route('/joy')
def joy_page():
	return render_template('ros/joystick.html')

from app import app, models