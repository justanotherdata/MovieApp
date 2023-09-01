from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from main.external_config.celery_worker import make_celery
from main.external_config.flask_cache import make_cache
from flask_cors import CORS
import redis
#from main.func import *

#from celery import Celery

import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'MySuPeRSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "../project.sqlite3")

app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/2"
app.config['CELERY_BACKEND'] = "redis://localhost:6379/3"

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'


cache = make_cache(app)
app.app_context().push()


celery = make_celery(app)
celery.conf.update({'broker_connection_retry_on_startup' : True})

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

loginmanager = LoginManager(app)


#This section is handling the Superadmin login which has been made using jinja2 templates
loginmanager.login_view = 'login_superadmin'
loginmanager.login_message_category = 'info'
loginmanager.login_message = 'Please Login As SuperAdmin To Proceed Further!'









#importing the routes
from main.api import superadmin, users, admins_copy