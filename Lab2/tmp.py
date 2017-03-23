import pywapi
import iot_yahoo_codes
#import serial
import pprint
from dashboard_emulation import Forecasts

pp = pprint.PrettyPrinter()

pp.pprint (pywapi.get_where_on_earth_ids("Stockholm, AB, Sweden"))
pp.pprint(pywapi.get_where_on_earth_ids("Krakow, MA, Polska"))
pp.pprint(pywapi.get_where_on_earth_ids("Istanbul, 34, Turkey"))

pp.pprint (pywapi.get_loc_id_from_weather_com("Stockholm")) #{'count': 2, 0: (LOCID1, Placename1), 1: (LOCID2, Placename2)}
pp.pprint (pywapi.get_loc_id_from_weather_com("Krakow")) #{'count': 2, 0: (LOCID1, Placename1), 1: (LOCID2, Placename2)}
pp.pprint (pywapi.get_loc_id_from_weather_com("Istanbul")) #{'count': 2, 0: (LOCID1, Placename1), 1: (LOCID2, Placename2)}

print "======================="
my_town_id, my_town_name = pywapi.get_loc_id_from_weather_com("Stockholm")[0]
pp.pprint(pywapi.get_weather_from_weather_com(my_town_id,'metric')) #input: my_town_id e.g. = 'PLXX0012'

print "======================="
my_town_id = pywapi.get_where_on_earth_ids("Stockholm").keys()[0]
pp.pprint(pywapi.get_weather_from_yahoo(my_town_id, 'metric')) #input: my_town_id e.g. = u'2500064'


forecastsObj = Forecasts()






