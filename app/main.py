from flask import Flask, render_template
from app.api import resume

app = Flask(__name__, template_folder='../templates')

app.register_blueprint(resume.bp, url_prefix="/resume")

@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")
