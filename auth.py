from flask import Blueprint, abort, request
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from globals import login_manager, db

auth = Blueprint("auth", __name__)

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key =True)
  username = db.Column(db.String(20), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable=False)
  
@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return abort(400)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

@auth.route("/register", methods=["GET", "POST"])
def register():
  username = request.form['username']
  if User.query.filter_by(username=username.data).first():
    return abort(418)
  return username
  

@auth.route("/login", methods=["GET", "POST"])
def login():
  return "login"