from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
import time
import json
import setting
import filterData
import redis 
import time
app= Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mining-data"
app.config['MONGO_HOST'] = setting.HOST
app.config['MONGO_PORT'] = setting.PORT
app.config['MONGO_USERNAME'] = setting.USERNAME
app.config['MONGO_PASSWORD'] = setting.PASSWORD
mongo = PyMongo(app)
db_redis = redis.StrictRedis(host=setting.REDIS_HOST,
    port=setting.REDIS_PORT, db = setting.REDIS_DB)


@app.route('/',methods=['GET'])
def Hello_Flask():
  return "Hello"
@app.route('/alltask',methods =['GET'])
def alltask():
  star = mongo.db.segmentID
  output = []
  for s in star.find():
    output.append({'segment_id' : s['segment_id']})
  return jsonify({'result' : output})
# @app.route('/testRedis' , methods =['GET'])
# def testRedis():
      
@app.route('/requestData',methods=['POST'])
def receivePrequest():
  data = {"success": False}
  outpredict = []
  if request.method == "POST" : 
    jsondata = request.get_json()
    segmentID = mongo.db.segmentID
    jsondataAddSegment = filterData.filterData(jsondata, segmentID)
    jsondataAddSegment_segmentID = []
    for x in jsondataAddSegment:
        print(x)
        jsondataAddSegment_segmentID.append(x["segment_id"])
        db_redis.rpush(setting.PREDIC_QUEUE, json.dumps(x))
    
    while True :
        if jsondataAddSegment_segmentID is not None :
            for segment in jsondataAddSegment_segmentID:
                output = db_redis.get(segment)
                print(output)
                if output is not None :
                    # print("ádjhjahsdjhas")
                    
                    output = output.decode("utf-8")
                    outpredict.append(json.loads(output))

                    db_redis.delete(segment) 
            break    
        time.sleep(setting.CLIENT_SLEEP)
    # return jsonify(jsondataAddSegment)
    return jsonify(outpredict)
  else : 
    return {"status-server":"wrong-methods"}




if __name__=="__main__":
    print("* Starting web service...")
    app.run(debug = True , host ='localhost' , port = 5000)



        # if output != None :
                    # output = output.decode("utf-8")
                    # data["predictions"] = json.loads(output)
                    # db_redis.delete(52241)
                    # break