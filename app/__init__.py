from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON
# from config import config
from  flask.ext.security import Security, SQLAlchemyUserDatastore
import os
from flask.ext.mail import Mail, Message

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = 'dotbot_ludovico'

# italy_time = pytz.timezone("Europe/Rome")

db = SQLAlchemy(app)

# bootstrap.init_app(app)


mail = Mail(app)
# user_datastore = SQLAlchemyUserDatastore(db, models.User, Role)
# security = Security(app, user_datastore)


from app.mainViews import mainViews
from app.userViews import userViews
from app.programViews import programViews
from app.fileViews import fileViews
from app.rosViews import rosViews
app.register_blueprint(rosViews)
app.register_blueprint(fileViews)
app.register_blueprint(programViews)
app.register_blueprint(mainViews)
app.register_blueprint(userViews)


# json = FlaskJSON()

# config[config_name].init_app(app)
# db.init_app(app)
# json.init_app(app)

#
# def create_app(config_name):
#
#
#     config[config_name].init_app(app)
#     bootstrap.init_app(app)
#     moment.init_app(app)
#     db.init_app(app)
#     json.init_app(app)
#
#     def get_version():
#         import subprocess, os
#         path = os.path.realpath(__file__)
#         p = subprocess.Popen('git describe --always', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.path.dirname(path))
#         ver = ""
#         for line in p.stdout.readlines():
#             ver =  line.rstrip()
#         retval = p.wait()
#         return ver
#
#     @app.context_processor
#     def utility_processor():
#     	return dict(version=get_version())

from app import app, models