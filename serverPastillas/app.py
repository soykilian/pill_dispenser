import json
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import time
import schedule
import atexit
import mimetypes
import os
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2
import numpy as np
from re import A
from flask import Flask, request, render_template, jsonify
import pandas
from datetime import datetime, timedelta
import pytz
import threading


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
    launch_schedulers()
    if next_dose == "NULL": 
        print("not ready")
        return ("{ \"message\": \"NOT TODAY\"}")
    response = jsonify(next_dose)
    return(response)

def run_continuously():
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def controller_ft():
    #cosaas
    print("CONTROLANDOO LA ZONA")
    return (schedule.CancelJob)

def launch_schedulers():
    next_dose = check_schedules()
    if next_dose == "NULL" :
        return 
    time_m = datetime.strptime(next_dose,"%H:%M")
    print(time_m)
    time_m = time_m - timedelta(hours=0, minutes=5)
    next_dose = time_m.strftime("%H:%M")
    print(next_dose)
    schedule.every().day.at("19:49").do(controller_ft)
    stop_run_continuously = run_continuously()
    print("BUENAS TARDES")


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
def get_image():
    camera = PiCamera()
    camera.resolution = (800, 600)
    time.sleep(0.1)
    camera.start_preview()
    time.sleep(5)
    camera.capture('./img/pruebis.jpg', resize=(640,480))
    camera.stop_preview()

def process_image():
    get_image()
    image = cv2.imread("./img/pruebis.jpg")
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])
    array_alpha = np.array([0.8])
    array_beta = np.array([-100.0])
    cv2.add(image, array_beta, image)       
    n = 0
    cv2.multiply(image, array_alpha, image)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blurred, 130,180, cv2.THRESH_BINARY)[1]
    cv2.imshow("thresh", thresh)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        n+=1
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Nro de objetos", n)
    return n
schedule.every().day.at("00:00").do(new_day)