#-*- coding:utf-8 -*-
import urllib.request
import json

def get_dust_data():
	url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?"
	key = "&serviceKey=Ji92rDuQa7LzPkIsqaz3cEpDl9gkD4kxHAjtElODSgrRbHh3Zk4qzDzqXtuy58uBMbXJ2w5b6FagJmRoE74Bhw%3D%3D"
	station_name = "stationName=" + "%EB%B0%B1%EC%84%9D%EB%8F%99" #백석동 주소
	#station_name = "sidoName=" + "%EB%B0%B1%EC%84%9D%EB%8F%99" #백석동 주소
	#station_name = "stationName=" + str(loc)
	data_term = "&dataTerm=month"
	page_no = "&pageNo=1"
	num_of_row = "&numOfRows=10"
	version = "&ver=" + "1.3"
	return_type = "&_returnType=json"

	api_url = url + station_name + data_term + page_no + num_of_row + key + version + return_type


	data = urllib.request.urlopen(api_url).read().decode('utf8')

	data_json = json.loads(data)
	
	parsed_json = data_json["list"][0]["pm10Value"]
	parsed_json = data_json['list'][0]['pm10Grade']
	# print(parsed_json)
	text = '-'

	if parsed_json == text:
		parsed_json = "없음"

	return parsed_json
#K = get_dust_data()
#print(K)
