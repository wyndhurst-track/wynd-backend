from flask import Flask, jsonify, request
from flask_cors import CORS

from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
				host="my-dbs-bp0.bristol.ac.uk",
				user="qy18694",
				password="Moocow21extended_",
				port=4407,
				database="wyndhurstfarm"
			)
  
cursor = db.cursor(prepared=True)

@app.route("/cows")
def cows_route():
  cursor.execute("SELECT cow_ID FROM data")
  cows = cursor.fetchall()
  return jsonify(cows)

@app.route("/data")
def data_route():
  cow_header = request.headers.get("cow-list")
  cow_list = cow_header.strip("[]").split(",")
  max_time = datetime.today().strftime("%Y-%m-%d")
  min_time = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
  query_params = cow_list
  query = "SELECT cx, cy, angle, detect_timestamp FROM data WHERE detect_timestamp BETWEEN '" + str(min_time) + " 00:00:00' AND '" + str(max_time) +" 00:00:00' AND cow_ID IN ({c})".format(c=', '.join(['%s'] * len(cow_list)))
  cursor.execute(query, query_params)
  data = cursor.fetchall()
  return jsonify(data)
