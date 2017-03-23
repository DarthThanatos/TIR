#!/usr/bin/env python

import pywapi
import serial
import pprint
from iot_yahoo_codes import patternMatchInputCondition

pp = pprint.PrettyPrinter(indent=4)

cities = ["Krakow", "Stockholm", "Istanbul"]
#button1: change city
#motion: change day

cityForecasts = {}

for city in cities:
    my_town_id = pywapi.get_where_on_earth_ids(city).keys()[0]
    result = pywapi.get_weather_from_yahoo(my_town_id, 'metric')
    dates = [d['date'] for d in result['forecasts']]
    conditions = [c['text'] for c in result['forecasts']]
    temperatures = [t['low'] for t in result['forecasts']]

    pp.pprint(dates)
    pp.pprint(conditions)
    pp.pprint(temperatures)
    cityForecasts[city] ={}
    for i in range(len(dates)):
        cityForecasts[city][dates[i]] = {}
        cityForecasts[city][dates[i]]["temperature"] = temperatures[i]
        cityForecasts[city][dates[i]]["condition"] = conditions[i]

pp.pprint(cityForecasts)

dashboardConditionMapping = {u'rainy': chr(27), u'sunny': chr(3), u'cloudy': chr(20), u'partly cloudy': chr(11)}

def mapTemperatureToRGB(temp):
    if temp <= -20:
        return 3  # b =3
    if temp <= -10:
        return 7  # g=3
    if temp <= 0:
        return 15  # r=1
    if temp <= 10:
        return 13
    if temp <= 20:
        return 60
    return 48

cityIndex = 0
city = cities[cityIndex]
dateIndex = 0
date = dates[dateIndex]

ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
ser.write(chr(128 + 16 + 1))  # subscribe motion and button 1

def setDevices():
    print "city:",city,"date:",date
    condition = cityForecasts[city][date]["condition"]
    conditionCategory = patternMatchInputCondition(condition)
    temperature = int(cityForecasts[city][date]["temperature"])
    ser.write(dashboardConditionMapping[conditionCategory])
    ser.write(chr(64 + mapTemperatureToRGB(temperature)))

try:
    while True:
        evt = ser.read(1)
        if len(evt) > 0:
            evt = ord(evt)
            if evt == (128 + 64 + 2 + 1):  # button 1 pressed
                cityIndex = (cityIndex + 1) % cities.__len__()
                city = cities[cityIndex]
                print "Pressed button, switched city to:", city
            elif evt == (128 + 64 + 1):
                dateIndex = (dateIndex + 1) % dates.__len__()
                date = dates[dateIndex]
                print "Motion detected, switched date to:", date
            else:
                continue
            setDevices()
except KeyboardInterrupt:
    ser.close()

