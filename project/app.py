from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
  #return "<p>Hello, World!</p>"
  return render_template('layout.html')