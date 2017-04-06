#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import sys
import mosquitto
import thread

preferences_dict = {}


def sendAvg():
    thermostats_amount = preferences_dict.keys().__len__()
    if thermostats_amount == 0:
        avg = 20
    else:
        sum = 0.0
        for preference in preferences_dict.values():
            sum += preference
        avg = int(sum/thermostats_amount)
    print "New average:", avg
    mqttc.publish(topic, str(avg), 0, False) #"temp/floor2/room1"

def on_connect(mqttc, obj, rc):
    #print("rc: "+str(rc))
    pass

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    if msg.payload == "broken":
        try:
            preferences_dict.__delitem__(msg.topic)
            print "removed", msg.topic
        except Exception:
            print "Ignoring broken msg"
    else:
        preferences_dict[msg.topic] = int(msg.payload)
    sendAvg()

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
    global ip, topic, pref_suffix, subs_topic
    ip = sys.argv[1]
    topic = sys.argv[2]
    subs_topic = topic + "/+"
except Exception:
    print "Usage: python controller.py ip publish_topic"
    exit()


mqttc.connect(ip, 1883, 60) #192.168.220.1
mqttc.subscribe(subs_topic, 0) #"temp/floor2/room1/+"
print "subscribed topic", subs_topic, "on server", ip, "\nPublishing average on", topic

mqttc.loop_forever()