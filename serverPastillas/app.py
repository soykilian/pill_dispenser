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
df = pandas.DataFrame(week_dict)
@app.route("/index", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/time", methods = ["GET", "POST"])
def time():
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
    print(body.decode())
    update_df(body.decode())
    return ("{ \"name\": \"diego\"}")


def update_dict(body) :
   for key in schedules_dict:
        if not(schedules_dict[key]):
            body.replace('"', '')
            schedules_dict[key] = body
            break

def update_df(body):
    row = []
    scheduler.start()
    values = body.split(',')
    for k in range(28):
        row.append(values[k])
        if (k + 1 ) % 7 == 0 :
            print(row)
            df.loc[len(df.index)] = row
            row = []
 
        
def compare_time(time1, time2):
    print("hoy toca dosis")
    x = datetime
    if not(time1) or not(time2):
        return 
    time2 = time2.strip('\"')
    act_hour,act_min,sec2 = time1.split(":")
    hour,min = time2.split(":")
    if act_hour == hour :
        if int(min) - int(act_min) < 5 :
            print("Se vienen drogitas en",  int(min) - int(act_min), "minutos" )

def check_schedules():
    now = datetime.now()
    day = now.weekday()
    print("numero dia", day)
    current_time = now.strftime("%H:%M:%S")
    for i in range(4):
        row = df.iloc[i]
        print(row)
        if row[day] == '1':
            compare_time(current_time, schedules_dict[hours[i]])


scheduler = BackgroundScheduler()
scheduler.add_job(func=check_schedules, trigger="interval", seconds=60)

