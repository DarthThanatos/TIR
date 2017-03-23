weather_conditions_codes = (
	('tornado',                 'rainy'),  # 0
	('tropical_storm',          'rainy'),  # 1
	('hurricane',               'rainy'),  # 2
	('severe_thunderstorms',    'rainy'),  # 3
	('thunderstorms',           'rainy'),  # 4
	('mixed_rain_and_snow',     'rainy' ),  # 5
	('mixed_rain_and_sleet',    'rainy' ),  # 6
	('mixed_snow_and_sleet',    'rainy' ),  # 7
	('freezing_drizzle',        'rainy' ),  # 8
	('drizzle',                 'rainy' ),  # 9
	('freezing_rain',           'rainy' ),  # 10
	('showers',                 'rainy' ),  # 11
	('showers',                 'rainy' ),  # 12
	('snow_flurries',           'rainy' ),  # 13
	('light_snow_showers',      'rainy' ),  # 14
	('blowing_snow',            'rainy' ),  # 15
	('snow',                    'rainy' ),  # 16
	('hail',                    'rainy' ),  # 17
	('sleet',                   'rainy' ),  # 18
	('dust',                    'cloudy' ),  # 19
	('fog',                     'cloudy' ),  # 20
	('haze',                    'cloudy' ),  # 21
	('smoky',                   'cloudy' ),  # 22
	('blustery',                'cloudy' ),  # 23
	('windy',                   'partly cloudy' ),  # 24
	('cold',                    'cloudy'   ),  # 25
	('clouds',                  'cloudy'),  # 26
	('mostly_cloudy_night',     'cloudy'),  # 27
	('mostly_cloudy_day',       'cloudy'),  # 28
	('partly_cloudy_night',     'cloudy'),  # 29
	('partly_cloudy_day',       'cloudy'),  # 30
	('clear_night',             'partly cloudy' ),  # 31
	('sun',                     'sunny' ),  # 32
	('fair_night',              'partly cloudy' ),  # 33
	('fair_day',                'partly cloudy'   ),  # 34
	('mixed_rain_and_hail',     'rainy' ),  # 35
	('hot',                     'sunny' ),  # 36
	('isolated_thunderstorms',  'rainy'),  # 37
	('scattered_thunderstorms', 'rainy'),  # 38
	('scattered_thunderstorms', 'rainy'),  # 39
	('scattered_showers',       'rainy' ),  # 40
	('heavy_snow',              'rainy' ),  # 41
	('scattered_snow_showers',  'rainy' ),  # 42
	('heavy_snow',              'rainy' ),  # 43
	('partly_cloudy',           'partly cloudy'),  # 44
	('thundershowers',          'rainy' ),  # 45
	('snow_showers',            'rainy' ),  # 46
	('isolated_thundershowers', 'rainy' ),  # 47
	('cloudy', 'cloudy' ),  # 48
	('mostly_cloudy',     'cloudy'),  # 49
	('sunny',     'sunny'),  # 50
)

def patternMatchInputCondition(input, inp_sep=" "):
	input = input.lower().replace(inp_sep,"_")
	for (i,j) in weather_conditions_codes:
		if i==input:
			print "found:",i,"returned",j
			return j
	print "Not found:",input,"returns rainy"
	return "rainy"
