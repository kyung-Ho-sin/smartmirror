import datetime
import pytz
import urllib.request
import json
import time

def get_api_date():
	standard_time = [3, 5, 8, 11, 14, 17, 20, 23]
	time_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H')

	check_time = int(time_now)
	time_count = 0
	day_calibrate = 0
	while not check_time in standard_time:
		check_time -= 1
		if check_time < 2:
			day_calibrate = 1
			check_time = 23

	if check_time <= 3:
		check_time = 23
		day_calibrate = 1
		time_count = 1

	if check_time > 3 and time_count == 0:
		check_time = check_time - 3

	if check_time < 10:
		check_time = '0' + str(check_time)
	check_time = str(check_time)
	

	date_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
	check_date = int(date_now) - day_calibrate
		
	return (str(check_date)), (str(check_time) + '00')

def get_weather_data():
	api_date, api_time = get_api_date()
	url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
	key = "serviceKey=Ji92rDuQa7LzPkIsqaz3cEpDl9gkD4kxHAjtElODSgrRbHh3Zk4qzDzqXtuy58uBMbXJ2w5b6FagJmRoE74Bhw%3D%3D"
	date = "&base_date=" + api_date
	time = "&base_time=" + api_time
	nx = "&nx=36"
	ny = "&ny=128"
	numOfRows = "&numOfRows=100"
	type = "&_type=json"
	api_url = url + key + date + time + nx + ny + numOfRows + type
	data = urllib.request.urlopen(api_url).read().decode('utf8')
	data_json = json.loads(data)

	parsed_json = data_json['response']['body']['items']['item']

	target_date = parsed_json[0]['fcstDate']
	target_time = parsed_json[0]['fcstTime']

	passing_data = {}

	for one_parsed in parsed_json:
		if one_parsed['fcstTime'] == target_time and one_parsed['fcstDate'] == target_date:
			passing_data[one_parsed['category']] = one_parsed['fcstValue']
	
	return passing_data

def get_weather_data_tmx():
	api_date, api_time = get_api_date()
	url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
	key = "serviceKey=Ji92rDuQa7LzPkIsqaz3cEpDl9gkD4kxHAjtElODSgrRbHh3Zk4qzDzqXtuy58uBMbXJ2w5b6FagJmRoE74Bhw%3D%3D"
	date = "&base_date=" + api_date
	time = "&base_time=" + "1100"
	nx = "&nx=36"
	ny = "&ny=128"
	numOfRows = "&numOfRows=100"
	type = "&_type=json"
	api_url = url + key + date + time + nx + ny + numOfRows + type
	data = urllib.request.urlopen(api_url).read().decode('utf8')
	data_json = json.loads(data)

	parsed_json = data_json['response']['body']['items']['item']

	target_date = parsed_json[0]['fcstDate']
	target_time = parsed_json[0]['fcstTime']

	passing_data = {}

	for one_parsed in parsed_json:
		if one_parsed['fcstTime'] == target_time and one_parsed['fcstDate'] == target_date:
			passing_data[one_parsed['category']] = one_parsed['fcstValue']

	tmx = passing_data['TMX']
	return tmx

def get_weather_data_tmn():
	api_date, api_time = get_api_date()
	url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
	key = "serviceKey=Ji92rDuQa7LzPkIsqaz3cEpDl9gkD4kxHAjtElODSgrRbHh3Zk4qzDzqXtuy58uBMbXJ2w5b6FagJmRoE74Bhw%3D%3D"
	date = "&base_date=" + api_date
	time = "&base_time=" + "0200"
	nx = "&nx=36"
	ny = "&ny=128"
	numOfRows = "&numOfRows=100"
	type = "&_type=json"
	api_url = url + key + date + time + nx + ny + numOfRows + type
	data = urllib.request.urlopen(api_url).read().decode('utf8')
	data_json = json.loads(data)

	parsed_json = data_json['response']['body']['items']['item']

	target_date = parsed_json[0]['fcstDate']
	target_time = parsed_json[0]['fcstTime']

	passing_data = {}

	for one_parsed in parsed_json:
		if one_parsed['fcstTime'] == target_time and one_parsed['fcstDate'] == target_date:
			passing_data[one_parsed['category']] = one_parsed['fcstValue']
	
	tmn = passing_data['TMN']
	return tmn

