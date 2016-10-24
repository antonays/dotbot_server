import os, json, sys, datetime
from flask import Blueprint
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import *

programViews = Blueprint('programViews', __name__)

@programViews.route('/getProgramDetails')
def getProgramDetails():
	try:
		programid = request.args.get('programid', None)
		program = Program.query.filter_by(program_id = programid).filter_by(isDeleted=False).first()
		program_files = File.query.filter_by(program_id=program.program_id).filter_by(isDeleted= False).all()
		files = [file.serialize() for file in program_files]
		return jsonify({"program": program.serialize(), "files": files})
	except:
		pass

@programViews.route('/add', methods=['GET','POST'])
def add():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	try:
		programname = request.args.get('prog_name')
		lang = request.args.get('prog_lang')
		newProgram = Program(user_id = session.get('loggedUser'), 
			program_name = programname, 
			language = lang,
			catkin_initialized = False,
			program_created = datetime.utcnow())
		db.session.add(newProgram)
		db.session.commit()
		flash("Program "+ newProgram.program_name+" Added Succesfully"+"~suc")
		return redirect(url_for('userViews.user_main', user=session.get('loggedUser')))
	except:
		flash("Program Was Not Added Succesfully"+"~err")
		return redirect(url_for('userViews.user_main', user=session.get('loggedUser')))

@programViews.route('/update', methods=['POST'])
def update():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	try:
		programid=request.form.get('program_id',None)
		if (programid == ""):
			return redirect (url_for('programViews.add', prog_name = request.form.get('prog_name', None),prog_lang = request.form.get('lang', None)))
		program_name=request.form['prog_name']
		lang=request.form['lang']
		updated_program = Program.query.filter_by(program_id=programid).filter_by(isDeleted= False).first()
		updated_program.program_name = program_name
		updated_program.language = lang
		db.session.commit()
		flash("Program "+ updated_program.program_name+" Updated Succesfully"+"~suc")
		return redirect(url_for('userViews.user_main', user=updated_program.user_id))
	except:
		not_updated_program = Program.query.filter_by(program_id=request.form['program_id']).filter_by(isDeleted= False).first()
		flash("Program "+ not_updated_program.user_name+" Was Not Updated Succesfully"+"~err")
		return redirect(url_for('userViews.user_main', user=not_updated_program.user_id))

@programViews.route('/delete', methods=['POST'])
def delete():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	try:
		programid=request.form['program_id']
		updated_program = Program.query.filter_by(program_id=programid).filter_by(isDeleted= False).first()
		updated_program_name = updated_program.program_name
		updated_program.isDeleted = True
		db.session.commit()
		flash("Program "+ updated_program_name+" Deleted Succesfully"+"~suc")
		return redirect(url_for('userViews.user_main', user=session.get('loggedUser')))
	except:
		not_updated_program = Program.query.filter_by(program_id=request.form['program_id']).filter_by(isDeleted= False).first()
		flash("Program "+ not_updated_program.program_name+" Was Not Deleted Succesfully"+"~err")
		return redirect(url_for('userViews.user_main', user=not_updated_program.user_id))


from app import app, models