#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import sys
import mosquitto
import thread

def on_connect(mqttc, obj, rc):
    #print("rc: "+str(rc))
    pass

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_publish(mqttc, obj, mid):
    #print("mid: "+str(mid))
    pass

def on_subscribe(mqttc, obj, mid, granted_qos):
    #print("Subscribed: "+str(mid)+" "+str(granted_qos))
    pass

def on_log(mqttc, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mosquitto.Mosquitto() 
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
#mqttc.connect("127.0.0.1", 1883, 60)

# setting testament for that client
#mqttc.will_set("temp/floor1/room1/pref1", "broken", 0, True)

try:
	global ip, topic  
	ip = sys.argv[1]
	topic = sys.argv[2]
except Exception:
	print "Usage: python therm2a.py ip topic"
	exit()

mqttc.connect(ip, 1883, 60) #192.168.220.1
mqttc.subscribe(topic, 0) #"temp/floor2/room1"
print "subscribed topic", topic, "on server", ip


def read_thread_func():
	while True:
		mqttc.loop_read(1)


def custom_loop():
	while True:
		msg = raw_input("Type the message you want to publish on topic temp/floor1/room1/pref1:\n")
		mqttc.publish("temp/floor1/room1/pref1", msg, 0, False)


#mqttc.loop_forever()
thread.start_new_thread(read_thread_func, ())
custom_loop()