#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import sys
import mosquitto
import thread
import serial

try:
    ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
    ser.write(chr(0b10000100))
    print "started"
except Exception:
    print "Could not open serial port"

def on_connect(mqttc, obj, rc):
    #print("rc: "+str(rc))
    pass

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    val = 20
    try:
        val = float(msg.payload)
        val = int((val - 16) / 16.0 * 31)
        ser.write(chr(0 | val))
        print "avg on hardware:", val
    except:
        pass


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


try:
    global ip, topic, pref_suffix
    ip = sys.argv[1]
    topic = sys.argv[2]
    pref_suffix = sys.argv[3]
except Exception:
    print "Usage: python therm.py ip subs_topic pref_suffix"
    exit()

pref_topic = topic + "/" + pref_suffix

# setting testament for that client
mqttc.will_set(pref_topic, "broken", 0, True)

mqttc.connect(ip, 1883, 60) #192.168.220.1
mqttc.subscribe(topic, 0) #"temp/floor2/room1"
print "subscribed topic", topic, "on server", ip, "\nPublishing preferences on", pref_topic

def hardware_loop():
    while True:
        try:
            cc = ser.read(1)
            if len(cc) < 1:
                continue
            cmd = ord(cc)    
            if cmd & 0b01000000 != 0:
                val = cmd & 0b00111111
                val = int(val / 64.0 * 16 + 16)
                mqttc.publish(pref_topic, str(val), 0, False)
        except Exception:
            pass

def custom_loop():
    while True:
        try:
            msg = input("Type the message you want to publish on topic " + pref_topic + ":\n")
            mqttc.publish(pref_topic, int(msg), 0, False) #"temp/floor2/room1/pref1"
        except Exception:
            print "not a valid integer value"

def read_thread_func():
    while True:
        mqttc.loop_read(1)

#mqttc.loop_forever())
thread.start_new_thread(read_thread_func, ())
custom_loop()