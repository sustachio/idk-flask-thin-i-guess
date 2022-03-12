from flask import Flask, render_template, Blueprint
from flask_login import login_required, current_user
from globals import login_manager, db
from auth import auth

app = Flask(__name__)

app.register_blueprint(auth, url_prefix="/auth")

def startup():
  # db setup
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" 
  app.config["SECRET_KEY"] = "JxIUtcbmGKlMMQgUFHuHNIKMraCnADRl"
  db.init_app(app)
  
  # auth setup
  
  login_manager.init_app(app)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/make")
def make():
  db.create_all()
  return "made"

if __name__ == '__main__':
  startup()
  app.run(debug=True, host='0.0.0.0', port=8089)