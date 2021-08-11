from flask import Flask, request
import psycopg2
from datetime import datetime, timedelta

# nothing special
app = Flask(__name__)

# same as consumer
pgConn = psycopg2.connect(host="postgres",
  database="numina",
  port="5432",
  user="postgres",
  password="postgres")

def pgQuery(sid, tt, start, end):
    if sid == -1: sid = str("*")
    if tt == "all": tt = str("*")
    if start is None: start = str("*")
    if end is None: end = str("*")

    cur = pgConn.cursor()
    cur.execute("SELECT * FROM metrics WHERE sensor_id=%s AND traveler_type=%s AND appears_at>=%s AND appears_at<=%s", (sid, tt, start, end))
    records = cur.fetchall()
    cur.close()
    return records

def getWindows(records):
    return

@app.route('/query', methods=["POST"])
def query():
    trav_type  = request.form.get("traveler_type")
    sensor_id = request.form.get("sensor_id")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")

    # basic error checking
    if (trav_type is None) or (sensor_id is None):
        abort(400)

    if start_time not is None: start_time = datetime.fromisoformat(start_time)
    if end_time not is None: end_time = datetime.fromisoformat(end_time)

    print("received query for sensor {}, type {}, {} until {}".format(sensor_id, trav_type, start_time, end_time))

    rec = pgQuery(int(sensor_id), trav_type, start_time, end_time)
    windows = getWindows(rec)

    #jsonify windows and return
