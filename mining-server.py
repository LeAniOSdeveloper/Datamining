import numpy as np
import setting
import datetime

import redis
import time
import json
import pickle
import joblib

db_predis = redis.StrictRedis(host=setting.REDIS_HOST,
	port=setting.REDIS_PORT, db = setting.REDIS_DB)
def map_WeekdayF(row):
  if row == "Monday" :
    return 0 
  elif  row == "Tuesday":
    return 1
  elif  row == "Wednesday":
    return 2
  elif row == "Thursday":
    return 3
  elif  row == "Friday":
    return 4
  elif row == "Saturday":
    return 5
  else  :
    return 6
def map_densityF(number):
  if  number == 4:
      return 'F'
  elif number == 3:
      return 'E'#'Dong Di Chuyen Cham'
  elif number == 2:
      return 'D'#'Dong Di Chuyen Duoc'
  elif number == 1 :
      return 'c'#'Dong Di Chuyen Binh Thuong'
  else:
      return 'A/B'#'Thong Thoang'
def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
def classify_process():
	print("load modoling ...")
	filename = "NGUYỄN HỮU THỌ TỪ ĐƯỜNG SỐ 15 ĐẾN CẦU KÊNH TẺ.pkl"
	model = joblib.load(filename)
	print("* Model loaded")
	while True : 
		queue = db_predis.lrange(setting.PREDIC_QUEUE , 0 , 1 )
		print(queue)
		output = []
		for q in queue:
			q = json.loads(q)
			
			day = map_WeekdayF(q['dayofWeek'])
			segment = q['segment_id']
			time1 = q["time"]
			get_sec(time1)
			print(day)
			print(get_sec(time1))
			print(segment)
			prediction = model.predict([np.array([segment,get_sec(time1),day])])
			print(map_densityF(prediction))
			r = {
				"segment_id" : segment,
				"lat" : q["lat"],
				"log" : q["log"],
				"time": time1 ,
				"dayofWeek"  : q['dayofWeek'],
				"prediction" : map_densityF(prediction)
			}
			print(r)
			db_predis.set(segment, json.dumps(r))
			db_predis.ltrim(setting.PREDIC_QUEUE, len(r), -1)
			time.sleep(setting.CLIENT_SLEEP)
		time.sleep(5)
if __name__ == "__main__":
	classify_process()