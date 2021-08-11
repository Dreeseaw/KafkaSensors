# For processing records via Redis & loading into Postgres
from datetime import datetime, timedelta
import pickle
from math import sqrt
import redis
import psycopg2

keystr = "{}/{}"

class TravObj(object):
    def __init__(self, tmp, px, py, ave=0.0, min=0.0, max=0.0, ct=0):
        self._tmp = tmp
        self._px  = px
        self._py  = px
        self._ave = ave
        self._min = min
        self._max = max
        self._ct  = ct

# inserts a row into metrics
def pgInsert(pgConn, tid, tobj, sid, typ):
    cur = pgConn.cursor()
    cur.execute("INSERT INTO metrics (traveler_id, traveler_type, sensor_id, appears_at, max_speed, min_speed, avg_speed) VALUES (%s, %s, %s, %s, %s, %s, %s)", (tid, typ, sid, tobj._tmp, tobj._max, tobj._min, tobj._ave))
    pgConn.commit()
    cur.close()
    print("added {} into postgres".format(tid))

# updates a metrics row
def pgUpdate(pgConn, tid, tobj):
    cur = pgConn.cursor()
    cur.execute("UPDATE metrics SET max_speed=%s, min_speed=%s, avg_speed=%s WHERE traveler_id=%s", (tobj._max, tobj._min, tobj._ave, tid))
    pgConn.commit()
    cur.close()
    print("updated {} into postgres".format(tid))

def process(redis, pgConn, sid, tid, typ, tmp, px, py):
    if not redis.exists(tid):
        # if key not in redis, insert into redis & done
        redis.set(tid, pickle.dumps(TravObj(tmp, px, py)), ex=60)

        # wait until spd can be calced to put into postgres
        print("added {} to redis".format(tid))
        return

    tobj = pickle.loads(redis.get(tid))

    # calc speed = sqrt(abs(px)^2 + abs(py)^2) / secs
    pxd = float(abs(px-tobj._px))
    pyd = float(abs(py-tobj._py))
    dist = float(sqrt((pxd*pxd)+(pyd*pyd))) # in feet
    fps = dist / (tmp-tobj._tmp).total_seconds()

    if tobj._ct == 0:
        tobj_new = TravObj(tmp, px, py, fps, fps, fps, 1)
        redis.set(tid, pickle.dumps(tobj_new), ex=60)
        # send this object to postgres & done
        pgInsert(pgConn, tid, tobj, sid, typ)
        print("first speed calc for {}".format(tid))
    elif tobj._ave == fps:
        # no postgres update needed, going average speed
        tobj._tmp = tmp
        tobj._px  = px
        tobj._py  = py
        tobj._ct  += 1
        redis.set(tid, pickle.dumps(tobj), ex=60)
        print("basic redis update for {}".format(tid))
    else: # now postgres will need an update
        tobj._ave = ((tobj._ave*tobj._ct)+fps)/(tobj._ct + 1)
        tobj._ct  += 1
        tobj._tmp = tmp
        tobj._px  = px
        tobj._py  = py
        if fps > tobj._max:
            tobj._max = fps
        elif fps < tobj._min:
            tobj._min = fps
        redis.set(tid, pickle.dumps(tobj), ex=60)
        print("mixed redis update for {}".format(tid))
        # todo: UPDATE postgres table
        pgUpdate(pgConn, tid, tobj)
