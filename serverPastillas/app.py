import json
import time
import atexit
import mimetypes
import os
from re import A
from flask import Flask, request, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import pandas
from datetime import datetime
import pytz

app = Flask(__name__)
schedules_dict = {
    "Desayuno" : "",
    "Comida" : "",
    "Cena" : "",
    "Noche" : "",
}

@app.route("/index", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/time", methods = ["GET", "POST"])
def time():
    if request.method == 'POST':
       body = request.data.decode()
       print(type(body))
       print("traza post")
       update_dict(body)
       print(schedules_dict)
       return ("{ \"name\": \"diego\"}")

    elif request.method == 'GET':
        print("traza GET_TIME1 ")
        json_sch = jsonify(schedules_dict)
        print("traza GET_TIME 2")
        return (json_sch)

def update_dict(body) :
   for key in schedules_dict:
        if not(schedules_dict[key]):
            body.replace('"', '')
            schedules_dict[key] = body
            break

def compare_time(time1, time2):
    print(time2)
    time2 = time2.strip('\"')
    act_hour,act_min,sec2 = time1.split(":")
    hour,min = time2.split(":")
    print("Hora actual", act_hour)
    print("Hora pastilli", hour)
    if act_hour == hour :
        if int(min) - int(act_min) < 5 :
            print("Se vienen drogitas en",  int(min) - int(act_min), "minutos" )

def check_schedules():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    for key in schedules_dict:
        if schedules_dict[key]:
            compare_time(current_time, schedules_dict[key])


scheduler = BackgroundScheduler()
scheduler.add_job(func=check_schedules, trigger="interval", seconds=10)
scheduler.start()            

