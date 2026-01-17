from flask import Flask, render_template
from app.api import resume
from app.models.database import db
from app.routes import auth_bp

app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillgenome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(resume.bp, url_prefix="/resume")

# Replace @app.before_first_request with app context initialization
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")
