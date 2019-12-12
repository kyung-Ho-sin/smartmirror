from . import get_weather_api
from . import get_dust_api
#import get_weather_api
#import get_dust_api


def dust_grade():
	dust_data = get_dust_api.get_dust_data()

	dust_grade_str = ''
	if dust_data == '1':
		dust_grade_str = '좋음'
	elif dust_data == '2':
		dust_grade_str = '보통'
	elif dust_data == '3':
		dust_grade_str = '나쁨'
	elif dust_data == '4':
		dust_grade_str = '매우나쁨'

	return dust_grade_str

def weather_parsing():
	weather_data = get_weather_api.get_weather_data()
	humidity = weather_data['REH']
	temperature = weather_data['T3H']
	sky_state = weather_data['SKY']
	rain_state = weather_data['PTY']
	#dust = dust_grade()	
	return [humidity, temperature, sky_state, rain_state]
		   #습도,       온도,         하늘상태   비상태
#C = weather_parsing()
#print(C)
