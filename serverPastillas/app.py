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
next_dose = ""
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
    return ("{ \"name\": \"diego\"}")

@app.route("/dose", methods=["GET"])
def dose():
    while len(next_dose) == 0:
        print("wait")
        time.sleep(1)
    print("saludis", next_dose)
    response = jsonify(next_dose)
    return(response)

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
    x = datetime
    time2 = time2.strip('\"')
    if len(time2) == 0:
        return 
    next_dose = time2
    print("TRAZA")
    print(next_dose)
    act_hour,act_min,sec2 = time1.split(":")
    hour,min = time2.split(":")
    if act_hour == hour :
        if int(min) - int(act_min) < 5 :
            print("Se vienen drogitas en",  int(min) - int(act_min), "minutos" )

def check_schedules():
    now = datetime.now()
    day = now.weekday()
    current_time = now.strftime("%H:%M:%S")
    if not(os.path.exists("data.csv")):
        print("not csv")
        return
    act_df = pandas.read_csv("data.csv")
    for i in range(4):
        row = df.iloc[i]
        if row[day] == '1':
            compare_time(current_time, row[7])

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_schedules, trigger="interval", seconds=1)
scheduler.start()

