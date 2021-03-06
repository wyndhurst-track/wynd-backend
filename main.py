from flask import Flask, jsonify, request
from flask_cors import CORS

from datetime import datetime, timedelta
import mysql.connector

import logging

log_to_file = 0

if log_to_file:
  log_dir = "/home/qy18694/logs/back-end/"
  log_file = datetime.today().strftime("%Y-%m-%d")
  log_path = log_dir + log_file
  logging.basicConfig(filename=log_path, level=logging.INFO)

def log_info(msg):
  log(logging.info, msg)

def log(log_fn, msg):
  # Create the string we want to log
  log_str = f" {datetime.now()} - {msg}"
  log_fn(log_str)

if log_to_file:
  log_info("Initialise logging")

def create_app():
  app = Flask(__name__)
  CORS(app)
  if log_to_file:
    log_info("Initialise Flask")
  return app

db = mysql.connector.connect(
        host="my-dbs-bp0.bristol.ac.uk",
        user="qy18694",
        password="Moocow21extended_",
        port=4407,
        database="wyndhurstfarm"
      )
if log_to_file:
  log_info("Initialise database connection")
cursor = db.cursor(prepared=True)

if __name__=='main':
  app = create_app()

@app.route("/cows")
def cows_route():
  if log_to_file:
    log_info("Receive request: /cows")
  req_begin = datetime.now()
  try:
    cursor.execute("SELECT DISTINCT cow_ID FROM data ORDER BY cow_ID")
    cows = cursor.fetchall()
  except:
    db = mysql.connector.connect(
        host="my-dbs-bp0.bristol.ac.uk",
        user="qy18694",
        password="Moocow21extended_",
        port=4407,
        database="wyndhurstfarm"
      )
    if log_to_file:
      log_info("Initialise database connection")
    cursor = db.cursor(prepared=True)
    cursor.execute("SELECT DISTINCT cow_ID FROM data ORDER BY cow_ID")
    cows = cursor.fetchall()
  req_end = datetime.now()
  timedelta = req_end - req_begin
  if log_to_file:
    log_info("Request resolve: " + str(timedelta.microseconds / 1000) + " miliseconds")
  return jsonify(cows)

@app.route("/data")
def data_route():
  cow_header = request.headers.get("cow-list")
  start_time = datetime.fromtimestamp(int(request.headers.get("start-time"))/1000).strftime("%Y-%m-%d")
  end_time = datetime.fromtimestamp(int(request.headers.get("end-time"))/1000).strftime("%Y-%m-%d")
  if log_to_file:
    log_info("Recieve request: /data " + cow_header + " " + start_time + " " + end_time)
  cow_list = cow_header.strip("[]").split(",")
  query_params = cow_list
  query = "SELECT cow_ID, cx, cy, angle, detect_timestamp FROM data WHERE detect_timestamp BETWEEN '" + str(start_time) + " 00:00:00' AND '" + str(end_time) +" 00:00:00' AND cow_ID IN ({c})".format(c=', '.join(['%s'] * len(cow_list)))
  try:
    cursor.execute(query, query_params)
    data = cursor.fetchall()
  except:
    db = mysql.connector.connect(
        host="my-dbs-bp0.bristol.ac.uk",
        user="qy18694",
        password="Moocow21extended_",
        port=4407,
        database="wyndhurstfarm"
      )
    if log_to_file:
      log_info("Initialise database connection")
    cursor = db.cursor(prepared=True)
    cursor.execute(query, query_params)
    data = cursor.fetchall()
  return jsonify(data)
