#!/usr/bin/env python

import pywapi
import pprint
from iot_yahoo_codes import patternMatchInputCondition

class Forecasts:
    def __init__(self, cities = ["Krakow", "Stockholm", "Istanbul"]):
        pp = pprint.PrettyPrinter(indent=4)
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
            cityForecasts[city] = {}
            for i in range(len(dates)):
                cityForecasts[city][dates[i]] = {}
                cityForecasts[city][dates[i]]["temperature"] = temperatures[i]
                cityForecasts[city][dates[i]]["condition"] = conditions[i]

        self.cities = cities
        self.dates = dates
        self.pp = pp
        self.cityForecasts = cityForecasts

    def printForecasts(self):
        self.pp.pprint(self.cityForecasts)

if __name__ == "__main__":
    cities = ["Krakow", "Stockholm", "Istanbul"]
    forecastsObj = Forecasts(cities)
    dates = forecastsObj.dates
    cityForecasts = forecastsObj.cityForecasts


    dashboardConditionMapping = {u'rainy': chr(27), u'sunny': chr(3), u'cloudy': chr(20), u'partly cloudy': chr(11)}


    def mapTemperatureToRGB(temp):
        if temp <= -25:
            return 3  # b =3
        if temp <= -10:
            return 7  # g=3
        if temp <= 0:
            return 15  # r=1
        if temp <= 10:
            return 13
        if temp <= 25:
            return 60
        return 48


    cityIndex = 0
    city = cities[cityIndex]
    dateIndex = 0
    date = dates[dateIndex]

    def emulateReactions(code,param):
        if ord(code) == 0:
            print "Wrote",ord(param),"to dashboard"
        elif ord(code) == 64:
            print "Set rgb to", ord(param)


    def setDevices():
        print "city:",city,"date:",date
        condition = cityForecasts[city][date]["condition"]
        conditionCategory = patternMatchInputCondition(condition)
        temperature = int(cityForecasts[city][date]["temperature"])
        emulateReactions(chr(0),dashboardConditionMapping[conditionCategory])
        emulateReactions(chr(64), chr(mapTemperatureToRGB(temperature)))


    while True:
        try:
            evt = input("Type int value: ")
            if evt == (128 + 64 + 2 + 1):  # button 1 pressed
                cityIndex = (cityIndex + 1) % cities.__len__()
                city = cities[cityIndex]
                print "Pressed button, switched city to:", city
            elif evt == (128 + 64 + 1):
                dateIndex = (dateIndex + 1) % dates.__len__()
                date = dates[dateIndex]
                print "Motion detected, switched date to:", date
            else:
                print "Your value does not match any of the subscribed devices"
                continue
            setDevices()
        except Exception:
            print "Not an int"
