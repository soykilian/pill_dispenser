import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/time", methods = ["GET", "POST"])
def time():
    if request.method == 'POST':
       body = request.data
       print("traza post")
       print(body)
       
       return ("{ \"name\": \"diego\"}")
    elif request.method == 'GET':
        return render_template("index.html")

