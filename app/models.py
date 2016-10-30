from . import db
from datetime import datetime
from os import path, mkdir, chmod
import stat, os
from flask import current_app, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

class File(db.Model):
	__tablename__ = "file"

	file_id = db.Column(db.Integer, primary_key=True)
	file_name = db.Column(db.String(128), unique=True, index=True)
	file_content = db.Column(db.Text, default="")
	program_id = db.Column(db.Integer, db.ForeignKey('program.program_id'))
	is_executable = db.Column(db.Boolean, default=False)
	last_edit = db.Column(db.DateTime, default=datetime.utcnow)
	isDeleted = db.Column(db.Boolean, default=False)

	def language(self):
		return self.file_name.split('.')[-1]

	def __repr__(self):
		return '<File %r>' % self.file_name

	def delete(self):
		os.remove(self.file_name)
		db.session.delete(self)
		db.session.commit()

	def to_json(self):
		json_file = {
			'id' : self.file_id,
			'filename' : path.basename(self.file_name),
			'last_edit' : self.last_edit,
			'program_id' : self.program_id
		}
		return json_file

	@staticmethod
	def from_json(json_file):
		file_name = json_file.get('file_name')
		content = json_file.get('content')
		return File(file_name=file_name, content=content)

	def serialize(self):
		return {
			'file_id':self.file_id,
			'file_name':self.file_name,
			'file_content':self.file_content,
			'program_id':self.program_id,
			'is_executable':self.is_executable,
			'last_edit':self.last_edit,
			'language':self.language()
		}


class Program(db.Model):
	__tablename__ = 'program'

	program_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	program_name = db.Column(db.String(255), unique=True, index=True)
	program_created = db.Column(db.DateTime, default=datetime.utcnow)
	catkin_initialized = db.Column(db.Boolean, default=False)
	language = db.Column(db.String(8), default='cpp')
	isDeleted = db.Column(db.Boolean, default=False)
	files = db.relationship('File', backref='program')

	def serialize(self):
		return {
			'program_id':self.program_id,
			'user_id':self.user_id,
			'program_name':self.program_name,
			'program_created':self.program_created,
			'catkin_initialized':self.catkin_initialized,
			'language':self.language
		}

	def create(self):
		if not self.exist():
			mkdir(self._folder());
			if self.language == 'cpp':
				main_file = File(file_name=path.join(self._folder(), 'node.' + self.language), program = self)
				main_file.program = render_template('code/default.cpp')
				dotbot_file = File(file_name=path.join(self._folder(), '.dotbot_ros'), program = self)
			else:
				main_file = File(file_name=path.join(self._folder(), 'node_' + str(self.program_id) + '.' + self.language), program=self, is_executable=True)
				main_file.program = render_template('code/default.py')
				dotbot_file = File(file_name=path.join(self._folder(), '__init__.py'), program = self)
			db.session.add(main_file,dotbot_file)
			db.session.commit()
			main_file.save()
			dotbot_file.save()

	def exist(self):
		return path.isdir(self._folder())

	def _folder(self):
		if self.language == 'cpp':
			return path.join(current_app.config["CATKIN_FOLDER"], 'src', current_app.config["DOTBOT_PACKAGE_NAME"], 'src_' + str(self.id))
		else:
			return path.join(current_app.config["CATKIN_FOLDER"], 'src', current_app.config["DOTBOT_PACKAGE_NAME"], 'script_' + str(self.id))

	def executable(self):
		if self.language == 'cpp':
			return 'src_' + str(self.program_id) + '_' + current_app.config["DOTBOT_PACKAGE_NAME"]+'_node'
		else:
			return 'node_' + str(self.program_id) + '.' + self.language

	def __repr__(self):
		return '<Program %r>' % self.program_name

	@staticmethod
	def from_json(json_node):
		title = json_node.get('title')
		language = json_node.get('language') or 'cpp'
		return Program(program_name=title, language=language)

	def to_json(self):
		json_node = {
			'id' : self.program_id,
			'name' : self.program_name,
			'created' : self.program_created,
			'files_cnt' : len(self.files),
			'language' : self.language
		}
		return json_node

class User(db.Model, UserMixin):
	__tablename__ = "user"

	id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(255))
	user_email = db.Column(db.String(255))
	user_pass_hashed = db.Column(db.String(255))
	member_since = db.Column(db.DateTime, default=datetime.utcnow)
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	isDeleted = db.Column(db.Boolean, default=False)

	programs = db.relationship('Program', backref='user')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.user_pass_hashed = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.user_pass_hashed, password)

	def __repr__(self):
		return '<User %r>' % self.user_name

	def __init__(self, username, email, password):
		self.user_name = username
		self.user_email = email
		self.user_pass_hashed = hashize(password)
		self.member_since = datetime.utcnow()

	def __init__(self):
		pass

	def __init__(self, myid, username, email):
		self.id = myid
		self.user_name = username
		self.user_email = email
		pass

	def setDeleted(self):
		self.isDeleted = True

	def getId(self):
		return self.id;

	def hashize(psw):
		return generate_password_hash(psw)

class Language(db.Model):
	__tablename__ = "language"

	language_id = db.Column(db.Integer, primary_key=True)
	language_name = db.Column(db.String(255))
	isDeleted = db.Column(db.Boolean, default=False)

class Bot():

	def __init__(self, n, d):
		self.name = n
		self.data = d