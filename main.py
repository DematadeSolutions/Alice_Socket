import websocket
import _thread
import time
import rel
from modules import *
import csv
import redis
from datetime import date

# Enter the client code
client_key = 'AB053908'

#Enter the session Id
api_key='vCJz5by25ZoH7jNgrk6huLc0UlRbC6itgeSE67ITWz0PhW7iVaJ9KbPTHC0gf8sDyCoRTbeS1ujIJWX8BQtTMSKdBjLEXzSn1Z2zixFfPkSeutMIOrO8KyQKbO2Oko2n'
print("date : ",date.today())
date="2022-09-08"
fileArr=[
    {"file":'NSE.csv',"filter":["EQ"],"filterIndex":2,"symbolIndex":0,"tokenIndex":4},
    {"file":'NFO.csv',"filter":["OPTIDX","FUTIDX"],"filterIndex":4,"symbolIndex":0,"tokenIndex":3},
    {"file":'MCX.csv',"filter":["FUTCOM"],"filterIndex":4,"symbolIndex":0,"tokenIndex":3},
    {"file":'CDS.csv',"filter":["FUTCUR"],"filterIndex":5,"symbolIndex":1,"tokenIndex":4},
    {"file":'INDICES.csv',"symbolIndex":0,"tokenIndex":2}
    ]
# fileArr=['INDICES.csv']
arr=[]
# OPTIDX|FUTIDX
# NSE

print("test : ","hello" in ["hello","heyy"])

count=0
for file in fileArr:
    fileData = open(file["file"])
    csvreader = csv.reader(fileData)
    for row in csvreader:
        if "filter" in file and row[file["filterIndex"]] not in file["filter"]:
            pass
        else:
        # elif (file["file"]=="NFO.csv" and row[10]==date) or file["file"]!="NFO.csv":
            count=count+1
            arr.append("{}|{}".format(row[file["symbolIndex"]],row[file["tokenIndex"]]))

print(arr)
print(count)
# NFO
# for file in fileArr:
#     file = open(file)
#     csvreader = csv.reader(file)
#     count=0
#     for row in csvreader:
#         # if row[4] not in arrt:
#         #     arrt.append(row[4])
#         if row[4] == "OPTIDX" or row[4] == "FUTIDX":
#             count=count+1
#             arr.append("{}|{}".format(row[0],row[3]))


# MCX
# for file in fileArr:
#     file = open(file)
#     csvreader = csv.reader(file)
#     count=0
#     for row in csvreader:
#         # if row[4] not in arrt:
#         #     arrt.append(row[4])
#         if row[4] == "FUTCOM":
#             count=count+1
#             arr.append("{}|{}".format(row[0],row[3]))

# CDS
# for file in fileArr:
#     file = open(file)
#     csvreader = csv.reader(file)
#     count=0
#     for row in csvreader:
#         # if row[5] not in arrt:
#         #     arrt.append(row[5])
#         if row[5] == "FUTCUR":
#             count=count+1
#             arr.append("{}|{}".format(row[1],row[4]))


# INDICES
# for file in fileArr:
#     file = open(file)
#     csvreader = csv.reader(file)
#     count=0
#     for row in csvreader:
#         count=count+1
#         arr.append("{}|{}".format(row[0],row[2]))

# print(arr)

# BSE,SENSEX,1 | NSE,NIFTY 50,26000 | NSE,NIFTY BANK,26009 | NSE,INDIA VIX,26017


# nsefile = open('NSE.csv')
# arr=[]
# csvreader = csv.reader(nsefile)
# count=0
# for row in csvreader:
#     if row[2] == "EQ":
#         count=count+1
#         arr.append("{}|{}".format(row[0],row[4]))

redis_client = redis.Redis(
    host= 'dematadesolutions.0yanxb.ng.0001.aps1.cache.amazonaws.com',
    port= '6379')

session_request=get_session(client_key,api_key)
if 'loginType' in session_request and session_request['loginType'] == None:
    print(session_request['emsg'])
else:
    session_id=session_request['sessionID']
    invalid_session=invalid_sess(client_key, session_id)
    if invalid_session['stat'] == 'Ok':
        print("Invalid Session request :",invalid_session['stat'])
        create_session=createSession(client_key, session_id)

        if create_session['stat'] == 'Ok':
            print("Create Session request  :",create_session['stat'])
            sha256_encryption1 = hashlib.sha256(session_id.encode('utf-8')).hexdigest()
            sha256_encryption2 = hashlib.sha256(sha256_encryption1.encode('utf-8')).hexdigest()

            def on_message(ws, message):
                # redis_client.set("AT-{}".format(feed_message["tk"]),json.dumps({"lp":feed_message["lp"],"pc":feed_message["pc"]}))
                data=json.loads(message)
                if "lp" in data and "tk" in data:
                    print(data)
                    redis_client.set("AT-{}".format(data["tk"]),data["lp"])
                    if "e" in data and (data["e"] == "NSE" or data["e"] == "BSE"):
                        redis_client.set("AT-PC-{}".format(data["tk"]),data["lp"])
                if 's' in data and data['s'] == 'OK':
                    for i in range(0,len(arr),200):
                        channel = "#".join(arr[slice(i,i+200)])
                        data = {
                            "k": channel,
                            "t": 't',
                            "m":"compact_marketdata"
                        }
                        ws.send(json.dumps(data))

            def on_error(ws, error):
                print(error)

            def on_close(ws, close_status_code, close_msg):
                print("### closed ###")

            def on_open(ws):
                print("Opened connection")
                initCon = {
                    "susertoken": sha256_encryption2,
                    "t": "c",
                    "actid": client_key + "_API",
                    "uid": client_key + "_API",
                    "source": "API"
                }
                ws.send(json.dumps(initCon))


            if __name__ == "__main__":
                websocket.enableTrace(False)
                ws = websocket.WebSocketApp("wss://ws1.aliceblueonline.com/NorenWS/",
                                          on_open=on_open,
                                          on_message=on_message,
                                          on_error=on_error,
                                          on_close=on_close)

                ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
                rel.signal(2, rel.abort)  # Keyboard Interrupt
                rel.dispatch()
