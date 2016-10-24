import os, json, sys, datetime
from flask import Blueprint
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import *

fileViews = Blueprint('fileViews', __name__)

@fileViews.route('/getFileDetails')
def getFileDetails():
	try:
		fileid = request.args.get('fileid', None)
		file = File.query.filter_by(file_id=fileid).filter_by(isDeleted= False).first()
		return jsonify(file.serialize())
	except:
		pass

from app import app, models