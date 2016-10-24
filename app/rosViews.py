import os, json, sys, datetime
from flask import Blueprint
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import *

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
    return render_template('ros/rosnodes.html', current_time=datetime.utcnow())

@rosViews.route('/rostopics')
def rostopics():
    return render_template('ros/rostopics.html', current_time=datetime.utcnow())

@rosViews.route('/rosconsole')
def rosconsole():
    return render_template('ros/rosconsole.html', current_time=datetime.utcnow())


@rosViews.route('/test')
def test_page():
    return render_template('ros/test.html')

@rosViews.route('/joy')
def joy_page():
    return render_template('ros/joystick.html')

from app import app, models