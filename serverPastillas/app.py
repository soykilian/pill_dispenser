import json
import time
import schedule
import atexit
import mimetypes
import os
from re import A
from flask import Flask, request, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import pandas
from datetime import datetime, timedelta
import pytz

app = Flask(__name__,
            static_url_path='',
            static_folder='static')
hours = ["Desayuno", "Comida", "Cena", "Noche"]
schedules_dict = {
    "Desayuno" : "",
    "Comida" : "",
    "Cena" : "",
    "Noche" : "",
}
week_dict = {
    "L": [],
    "M": [],
    "X": [],
    "J": [],
    "V": [],
    "S": [],
    "D": []
}
global next_dose
next_dose = ""
act = "init"
df = pandas.DataFrame(week_dict)

@app.route("/index", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/time", methods = ["GET", "POST"])
def time_pet():
    if request.method == 'POST':
       body = request.data.decode()
       update_dict(body)
       return ("{ \"name\": \"diego\"}")

    elif request.method == 'GET':
        json_sch = jsonify(schedules_dict)
        return (json_sch)

@app.route("/week", methods=["POST"])
def week():
    body = request.data
    update_df(body.decode())
    return ("{ \"message\": \"READY\"}")

@app.route("/dose", methods=["GET"])
def dose():
    next_dose = check_schedules()
    print("next_dose:",next_dose)
    if next_dose == "NULL": 
        print("not ready")
        return ("{ \"message\": \"NOT TODAY\"}")
    response = jsonify(next_dose)
    return(response)

def launch_schedulers():
    next_dose = check_schedules()
    if next_dose == "NULL" :
        return 
    time_m = time.strptime(next_dose,"%H:%M")
    time_m = time_m - timedelta(hours=0, minutes=5)
    next_dose = time_m.strftime("%H:%M")
    schedule.at(next_dose).do(controller_ft)

def controller_ft():
    #cosaas
    print("CONTROLANDOO LA ZONA")
    launch_schedulers()
    return schedule.CancelJob

def new_day():
    launch_schedulers()
    return schedule.CancelJob

def update_dict(body) :
   for key in schedules_dict:
        if not(schedules_dict[key]):
            body.replace('"', '')
            schedules_dict[key] = body
            break

def update_df(body):
    row = []
    values = body.split(',')
    for k in range(28):
        row.append(values[k])
        if (k + 1) % 7 == 0:
            df.loc[len(df.index)] = row
            row = []
    times = []
    for k in schedules_dict:
        times.append(schedules_dict[k])
    df["times"] = times
    df.to_csv("data.csv")

def compare_time(time1, time2):
    time2 = time2.strip('\"')
    return time2 > time1

def check_schedules():
    now = datetime.now()
    day = now.weekday()
    current_time = now.strftime("%H:%M")
    if not(os.path.exists("data.csv")):
        return
    act_df = pandas.read_csv("data.csv")
    act = "init"
    for i in range(4):
        row = act_df.iloc[i]
        if row[day+1] == 1:
            act = row[8]
            if compare_time(current_time, act) == True :
                return (act)
    return "NULL"

schedule.every().day.at("00:00").do(new_day)