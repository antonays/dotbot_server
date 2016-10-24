import os, json, sys, datetime
from flask import Blueprint
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import *
from .util import send_email

userViews = Blueprint('userViews', __name__)

@userViews.route('/user_main', methods=['GET'])
def user_main():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	try:
		userid = request.args.get('user')
		user = User.query.filter_by(id=userid).filter_by(isDeleted= False).first()
		user_programs = Program.query.filter_by(user_id=userid).filter_by(isDeleted= False).all()
		programs=list()
		for program in user_programs:
			program_files = File.query.filter_by(program_id=program.program_id).filter_by(isDeleted= False).all()
			prog_files_tuple = program, program_files
			programs.append(prog_files_tuple)
		languages = Language.query.filter_by(isDeleted = False).all()
		return render_template('user_main.html', connected_user=user, user_programs=programs, languages = languages)
	except:
		flash("user panel failed"+"~err")
		return render_template('home.html', error = "")

@userViews.route('/from_session', methods=['GET'])
def from_session():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	userid = session.get('loggedUser');
	return redirect(url_for('userViews.user_main', user=userid))

@userViews.route('/register', methods=['POST'])
def register():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	try:
		username=request.form['username']
		email=request.form['email']
		password=request.form['pass']
		new_user = User(username,email,password)
		db.session.add(new_user)
		db.session.commit()
		return render_template('home.html', error="")
	except:
		flash("User Registration Failed"+"~err")
		return render_template('home.html', error = "")

@userViews.route('/update', methods=['POST'])
def update():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	try:
		userid=request.form['user_id']
		username=request.form['username']
		email=request.form['useremail']
		updated_user = User.query.filter_by(id=userid).filter_by(isDeleted= False).first()
		updated_user.user_name = username
		updated_user.user_email = email
		db.session.commit()
		flash("User "+ updated_user.user_name+" Updated Succesfully"+"~suc")
		return redirect(url_for('userViews.user_main', user=updated_user.id))
	except:
		not_updated_user = User.query.filter_by(id=request.form['user_id']).filter_by(isDeleted= False).first()
		flash("User "+ not_updated_user.user_name+" Was Not Updated Succesfully"+"~err")
		return redirect(url_for('userViews.user_main', user=not_updated_user.id))

@userViews.route('/delete', methods=['POST'])
def delete():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	try:
		userid=request.form['user_id']
		updated_user = User.query.filter_by(id=userid).filter_by(isDeleted= False).first()
		updated_user.isDeleted = True
		name = updated_user.user_name
		db.session.commit()
		flash("User "+ name+" Deleted Succesfully"+"~suc")
		return redirect('/')
	except:
		not_updated_user = User.query.filter_by(id=request.form['user_id']).filter_by(isDeleted= False).first()
		flash("User "+ not_updated_user.user_name+" Was Not Deleted Succesfully"+"~err")
		return redirect(url_for('userViews.user_main', user=not_updated_user.id))

@userViews.route('/p_update', methods=['POST'])
def p_update():
	if not session.get('loggedUser'):
		return flask.redirect(flask.url_for('/'))
	try:
		userid=request.form['user_id']
		updated_user = User.query.filter_by(id=userid).filter_by(isDeleted= False).first()
		old=request.form['oldpass']
		if(updated_user.verify_password(old)):
			new1=request.form['newpass1']
			new2=request.form['newpass2']
			if (new1 == new2):
				updated_user.password = new1
				db.session.commit()
				flash("Password changed succesfully, please login again"+"~suc")
				return redirect('logout')
			else:
				flash("Password Was Not Updated Succesfully - Passwords do not match"+"~err")
				return redirect(url_for('userViews.user_main', user=updated_user.id))
		else:
			flash("Password Was Not Updated Succesfully - Old password is invalid"+"~err")
			return redirect(url_for('userViews.user_main', user=updated_user.id))
	except:
		not_updated_user = User.query.filter_by(id=request.form['user_id']).filter_by(isDeleted= False).first()
		flash("Password was not updated due to unexpected error"+"~err")
		return redirect(url_for('userViews.user_main', user=updated_user.id))

@userViews.route('/pass_reset', methods=['POST'])
def pass_reset():
	useremail = request.form['email']
	userFound = User.query.filter_by(user_email=useremail).filter_by(isDeleted= False).first()
	if userFound is None:
		return redirect(url_for('mainViews.show_main', error = 'Not Such user Exists'))
	else:
		subject = "Password reset requested"
		# token = ts.dumps(user.email, salt='recover-key')
		# recover_url = url_for('userViews.reset_with_token',_external=True)
		html = render_template('pass_recovery.html')    
		send_email.send_email(useremail, subject, html)    
		return redirect(url_for('mainViews.show_main', error='Email Sent'))

@userViews.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('signin'))

    return render_template('reset_with_token.html', form=form, token=token)

from app import app, models