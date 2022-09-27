from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:\\Users\\tipiy\\Desktop\\Utilities\\Py-WebApp\\market\\market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# The login_view is automatically direct you to login page if you are not logged in.
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from market import routes