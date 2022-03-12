from flask import Blueprint, abort, request
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from globals import login_manager, db

auth = Blueprint("auth", __name__)


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key =True)
  username = db.Column(db.String(20), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable=False)
  
@login_manager.unauthorized_handler
def unauthorized():
    return "please log in"

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


@auth.route("/getuser", methods=["GET"])
@login_required
def getuser():
  return current_user.username

@auth.route("/register", methods=["GET", "POST"])
def register():
  username = request.form["username"]
  password = request.form["password"]
  
  if User.query.filter_by(username=username).first():
    return "failed"
  
  new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

  db.session.add(new_user)
  db.session.commit()

  return f"{username} {password} {generate_password_hash(password, method='sha256')}"
  

@auth.route("/login", methods=["GET", "POST"])
def login():
  username = request.form["username"]
  password = request.form["password"]

  user = User.query.filter_by(username=username).first()

  if not user:
    return "could not find user"
  if not check_password_hash(user.password, password):
    return "wrong password"

  login_user(user)
  
  return "loged in"

@auth.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
  logout_user()
  return "loged out"