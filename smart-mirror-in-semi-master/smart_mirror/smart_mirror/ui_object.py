from weather import weather_data_handler, timer
from caldavclient import schedule_handler
from mirror_Ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys, time, json
import activate_env_speech
import hashlib


"""
def show_schedule():
	t.mirror.ment_lb.setText("비밀문장을 말해주세요")
	activate_env_speech.activate()
	t.mirror.ment_lb.setText("비밀문장 입력이 완성되었습니다")
	with open('/home/pi/smart_mirror/text_directory/speech_text.txt', 'r') as f:
		mic_text = f.read()
	has_func = hashlib.md5()
	has_func.update(mic_text)
	mic_text = has_func.hexdigest()
	with open('/home/pi/smart_mirror/text_directory/user_info.json') as t:
		user_info_json = json.load(t)
	if mic_text in user_info_json:
		user_info_list = user_info_json[mic_text]
	else:
		t.mirror.ment_lb.setText("비밀문장이 틀렸습니다")
		show_schedule()
"""	


weather_list = []
timer_hour = ""
timer_min = ""
timer_sec = ""

with open('/home/pi/smart_mirror/text_directory/ment_handler.json') as t:
	ment_json = json.load(t)

#def str_to_method(str):
#	return getattr(sys.modules[__name__], str)


def get_info():
	global weather_list, timer_hour, timer_min, timer_sec, ment_string
	weather_list = weather_data_handler.weather_parsing()
	weather_list.append(weather_data_handler.dust_grade())
	timer_hour = timer.hour_slice()
	timer_min = timer.min_slice()
	timer_sec = timer.sec_slice()

class Form:
	def __init__(self):
		self.mirror = Ui_MainWindow()
		self.app, self.MainWindow, self.ui = setup()
		self.mirror.setupUi(self.MainWindow)
		self.user = ''

	def start_ui(self):
		self.MainWindow.show()
		sys.exit(self.app.exec_())

	def printer(self):
		print("!!!!!!!!")

	def update_info(self):
		while True:
			get_info()
			self.reset_init()
			self.image_select()
			time.sleep(5)
	def update_speech(self, function):
		while True:
			self.mirror.ment_lb.setText("안녕하세요 세미입니다")
			activate_env_speech.activate()
			with open('/home/pi/smart_mirror/text_directory/speech_text.txt', 'r') as f:
				self.mic_text = f.read()

			if self.mic_text == '그만할래':
				self.MainWindow.close()
				break
			if self.mic_text in ment_json:
				self.ment_method = function(ment_json[self.mic_text])
				self.ment_method()

			with open('/home/pi/smart_mirror/text_directory/speech_text.txt', 'w') as f:
				f.write("")

	def image_select(self):
		global weather_list

		if weather_list[3] == 0:
			#pass 이미지관련 문제생기면 이걸 주석해제
			if weather_list[2] == 1:
				pixmap = QPixmap("./picture/sun.png")
				self.mirror.weather_icon_lb.setPixmap(QPixmap(pixmap))
			elif weather_list[2] == 3:
				pixmap = QPixmap("./picture/cloud.png")
				self.mirror.weather_icon_lb.setPixmap(QPixmap(pixmap))
			elif weather_list[2] == 4:
				pixmap = QPixmap("./picture/cloudy.png")
				self.mirror.weather_icon_lb.setPixmap(QPixmap(pixmap))
		elif weather_list[3] == 1:
			pixmap = QPixmap("./picture/rain.png")
			self.mirror.weather_icon_lb.setPixmap(QPixmap(pixmap))
		elif weather_list[3] == 2:
			pixmap = QPixmap("./picture/snow_rain.png")
			self.mirror_weather_icon_lb.setPixmap(QPixmap(pixmap))
		elif weather_list[3] == 3:
			pixmap = QPixmap("./picture/snow.png")
			self.mirror.weather_icon_lb.setPixmap(QPixmap(pixmap))
		elif weather_list[3] == 4:
			picmap = QPixmap("./picture/rain.png")
			self.mirror.weather_icon_lb.setPixmap(QPixmap(pixmap))

	def reset_init(self):
		global timer_hour, timer_min, weather_list, timer_sec, ment_string
		self.mirror.time_lb.setText("  " + timer_hour + ":" + timer_min + ":" + timer_sec)
		self.mirror.wetness_lb.setText("  습도  " + str(weather_list[0]) + "%")
		self.mirror.temperature_lb.setText("  온도  " + str(weather_list[1]) + "°C")
		self.mirror.dust_lb.setText("미세먼지 " + str(weather_list[4]))


t = Form()
