import os, json, sys, datetime, socket
from flask import Blueprint
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import *
import flask_login, flask
from dbHandle import *

mainViews = Blueprint('mainViews', __name__)

@mainViews.route('/')
@mainViews.route('/main')
def show_main():
	error = request.args.get('error')
	if error is not None:
		return render_template('home.html', error=error)
	else:
		return render_template('home.html', error=[])

@mainViews.route('/login', methods=['GET', 'POST'])
def login():
	user = flask.request.form['username']
	ret = User.query.filter_by(user_name=user).filter_by(isDeleted= False).first()
	if (ret is None):
		error = "Username entered is invalid"
		return render_template('home.html', error=error)
	if check_password_hash(ret.user_pass_hashed, flask.request.form['password']):
		session["loggedUser"] = ret.id
		session["loggedUserName"] = ret.user_name
		ret.last_seen = datetime.utcnow()
		db.session.commit()
		flash(ret.user_name+" Connected Succesfully"+"~inf")
		return redirect(url_for('userViews.user_main', user=ret.getId()))
	else:
		error = "Password entered is invalid"
	return render_template('home.html', error=error)

@mainViews.route('/logout', methods=['GET', 'POST'])
def logout():
	session["loggedUser"] = None
	return render_template('home.html')

@mainViews.route('/get_ip', methods=['GET'])
def get_ip():
	try:
		myip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
		return (myip)
	except:
		return None

@mainViews.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings/settings.html', hostname=socket.gethostname(), ip= get_ip())
	

from app import app, models
