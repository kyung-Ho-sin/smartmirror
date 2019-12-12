import datetime


def year_slice():		#년도
	time_now = str(datetime.datetime.now())
	year_now = time_now[0:4]
	return year_now

def month_slice():		#월
	time_now = str(datetime.datetime.now())
	mon_now = time_now[5:7]
	return mon_now

def day_slice():		#일
	time_now = str(datetime.datetime.now())
	day_now = time_now[8:10]
	return day_now

def hour_slice():		#시간
	time_now = str(datetime.datetime.now())
	hour_now = time_now[11:13]
	return hour_now

def min_slice():		#분
	time_now = str(datetime.datetime.now())
	min_now = time_now[14:16]
	return min_now

def sec_slice():		#초
	time_now = str(datetime.datetime.now())
	sec_now = time_now[17:19]
	return sec_now

def get_week_name():	#요일
	dayString = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
	return dayString[datetime.date(int(year_slice()), int(month_slice()), int(day_slice())).weekday()]

