from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'warning'

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
from flaskblog.errors.handler import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)

