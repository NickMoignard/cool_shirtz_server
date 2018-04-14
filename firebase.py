#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:10:53 2018

@author: Nick Moignard
"""
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import db   
import json
from sys import argv
from datetime import datetime
import pytz

cred = credentials.Certificate("cool_cert.json")
app = firebase_admin.initialize_app(cred, { 'databaseURL': 'https://cool-shirtz.firebaseio.com'})

def toString(x):
    return str(x)

def update_topic_registrations():
    topics = map(toString, range(21))
    tokens = {}
    for topic in topics:
        tokens[topic] = []

    # get database reference
    ref = db.reference('/')
    
    # get user data
    snapshot = ref.get()

    # parse
    users = snapshot["users"]
    for key,val in users.items():
        tokens[str(val['numTimesPerDay'])].append(key)

    # register each topic
    for topic,tokens in tokens.items():
        if tokens != []:
            token_reg_res = messaging.subscribe_to_topic(tokens, topic)
            print(token_reg_res)
        else:
            print("'{}' Topic Empty".format(topic))

messages = [('dads', 'house'), ('wow', 'I think im dead'), ('HELP', 'send a message to my wife carla!'), ('that damned smile', 'i should never have trusted her')]

def send_notification(topic):
    message = random.choice(messages)
    title = message[0]
    body = message[1]
    message = messaging.Message(
        notification = messaging.Notification(
            title=title,
            body=body
        ), 
        topic=topic
    )
    res = messaging.send(message)
    print('message response : {}'.format(res))

message_roster = {}
topics = map(toString, range(21))
for topic in topics:
    message_roster[topic] = []
    for i in range(int(topic)):
        delta_hours = int(23 / int(topic))
        message_roster[topic].append(  (19 + delta_hours * i) % 24 )
    print(message_roster[topic])
    print(topic)

def schedule_messages():
    tz = pytz.timezone("Australia/Melbourne")
    aware_time = tz.localize(datetime.now())
    hour = int(aware_time.strftime("%H"))

    for topic, hours in message_roster.items():
        if hour in hours:
            print('send')
            #send message
            send_notification(topic)

if __name__ == "__main__":
    schedule_messages()
