# -*- coding: utf-8 -*-
import json
import logging
import os
import uuid
from io import BytesIO

import flask 
from flask import Flask,request
import requests 
from pya3 import *
import redis

app = flask.Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf'}

redis_client = redis.Redis(
    host= 'dematadesolutions.0yanxb.ng.0001.aps1.cache.amazonaws.com',
    port= '6379')

alice = Aliceblue(user_id='661371', api_key='TXKMMyVsUg9Re4MqVK3GN1mM18JdtAmsqSxTMXPrarvYLeqKLnbH0bGlo8EfZs30c4usiv6eogi5kmXfr7fWRJknOJFfQjDnpya8khaGi6SXodYm4dPLkYuDMstqAmeI')

LTP = 0
socket_opened = False
subscribe_flag = False
subscribe_list = []
unsubscribe_list = []

def socket_open():  # Socket open callback function
    print("Connected")
    global socket_opened
    socket_opened = True
    if subscribe_flag:  # This is used to resubscribe the script when reconnect the socket.
        alice.subscribe(subscribe_list)


def socket_close():  # On Socket close this callback function will trigger
    global socket_opened, LTP
    socket_opened = False
    LTP = 0
    print("Closed")


def socket_error(message):  # Socket Error Message will receive in this callback function
    global LTP
    LTP = 0
    print("Error :", message)


def feed_data(message):  # Socket feed data will receive in this callback function
    global LTP, subscribe_flag
    feed_message = json.loads(message)
    if feed_message["t"] == "ck":
        print("Connection Acknowledgement status :%s (Websocket Connected)" %
            feed_message["s"])
        subscribe_flag = True
        print("subscribe_flag :", subscribe_flag)
        print("-------------------------------------------------------------------------------")
        pass
    elif feed_message["t"] == "tk":
        print("Token Acknowledgement status :%s " % feed_message)
        print("-------------------------------------------------------------------------------")
        pass
    else:
        if 'lp' in feed_message:
            redis_client.set("AT-{}".format(feed_message["tk"]),feed_message["lp"])
            print("Feed :", feed_message)

        LTP = feed_message[
            'lp'] if 'lp' in feed_message else LTP  # If LTP in the response it will store in LTP variable

            
@app.route('/', methods=['GET'])
def home():
    symbol=request.args.get('symbol')

    print("API is Working",request)
    # print("API is Working",request.args.get('language'))

    # alice = Aliceblue(user_id='AB053908',
    #                   api_key='vCJz5by25ZoH7jNgrk6huLc0UlRbC6itgeSE67ITWz0PhW7iVaJ9KbPTHC0gf8sDyCoRTbeS1ujIJWX8BQtTMSKdBjLEXzSn1Z2zixFfPkSeutMIOrO8KyQKbO2Oko2n')
    print("session id : ", alice.get_session_id())  # Get Session ID
    # alice.get_contract_master("MCX")
    # alice.get_contract_master("NFO")
    # alice.get_contract_master("NSE")
    # alice.get_contract_master("BSE")
    # alice.get_contract_master("CDS")
    # alice.get_contract_master("BFO")
    # alice.get_contract_master("INDICES")

    # Socket Connection Request
    alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
                        socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True)

    while not socket_opened:
        pass
    #global subscribe_list, unsubscribe_list

    subscribe_list = [alice.get_instrument_by_token("NSE", 26000),alice.get_instrument_by_token("NSE", 26009)]
    print("subscribe : ",subscribe_list)
    alice.subscribe(subscribe_list)
    # if "data" in symbol and "Exchange" in symbol["data"] and "Token" in symbol["data"]:
    #     subscribe_list = [alice.get_instrument_by_token(symbol["data"]["Exchange"], symbol["data"]["Token"])]
    #     print("subscribe : ",subscribe_list)
    #     alice.subscribe(subscribe_list)
    print(datetime.now())
    sleep(10)
    print(datetime.now())
    # unsubscribe_list = [alice.get_instrument_by_symbol("NSE", "RELIANCE")]
    # alice.unsubscribe(unsubscribe_list)
    # sleep(8)

    # Stop the websocket
    # alice.stop_websocket()
    sleep(10)
    print(datetime.now())

    # Connect the socket after socket close
    alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
                        socket_error_callback=socket_error, subscription_callback=feed_data)


    return "API is Working"


if __name__ == '__main__':



    


    # Socket Connection Request
    alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
                        socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True)

    while not socket_opened:
        pass
    #global subscribe_list, unsubscribe_list

    subscribe_list = [alice.get_instrument_by_token("NSE", 26000),alice.get_instrument_by_token("NSE", 26009)]
    print("subscribe : ",subscribe_list)
    alice.subscribe(subscribe_list)
    # if "data" in symbol and "Exchange" in symbol["data"] and "Token" in symbol["data"]:
    #     subscribe_list = [alice.get_instrument_by_token(symbol["data"]["Exchange"], symbol["data"]["Token"])]
    #     print("subscribe : ",subscribe_list)
    #     alice.subscribe(subscribe_list)
    print(datetime.now())
    sleep(10)
    print(datetime.now())
    # unsubscribe_list = [alice.get_instrument_by_symbol("NSE", "RELIANCE")]
    # alice.unsubscribe(unsubscribe_list)
    # sleep(8)

    # Stop the websocket
    # alice.stop_websocket()
    sleep(10)
    print(datetime.now())

    # Connect the socket after socket close
    alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
                        socket_error_callback=socket_error, subscription_callback=feed_data)
                        
    # app.run(host='0.0.0.0')
