from tkinter import W
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_autoindex import AutoIndex

import json
import os
import threading
import requests
import sys
import shutil

import pandas as pd
import numpy as np

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_NAME = 'static'
STATIC_PATH = os.path.join(CURRENT_PATH, STATIC_NAME)

app = Flask(__name__,
        static_url_path = '',
        static_folder = 'static')
CORS(app)
@app.route('/')
def home():
   return render_template('/interface.html')


@app.route('/get_schedule', methods=['POST'])
def save_inputs():
    data = request.data
    print(data)
    return (data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
