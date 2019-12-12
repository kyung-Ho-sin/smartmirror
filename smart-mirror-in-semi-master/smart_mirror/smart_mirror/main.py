import time
import os, sys, json
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from mirror_Ui import *
import activate_env_speech
from weather import weather_data_handler, timer
from caldavclient import schedule_handler
from socket import *
from user_app.server import *
#sys.path.insert(0, '/home/pi/python-docs-samples/speech/microphone/')
#from transcribe_streaming_mic import text 


id_list = {'오늘나의할일은' : ['gill1994', '!@qwashin127845']}


scheduler_class = schedule_handler.Handler_parse()
#("gill1994", "as14736945")
scheduler = []
scheduler_string = ""
weather_list = []
timer_hour = ""
timer_min = ""
timer_sec = ""



with open('/home/pi/smart_mirror/text_directory/ment_handler.json') as t:
	ment_json = json.load(t)
	
def str_to_method(str):
	return getattr(sys.modules[__name__], str)

def reset_scheduler(user):
	global scheduler_string, id_list, scheduler
	scheduler = scheduler_class.parseInfo(id_list[user][0], id_list[user][1])
	scheduler.sort()
	scheduler_string = ""
	for x in scheduler:
		scheduler_string += x
		scheduler_string += "\n\n"
	

def get_info():
	global weather_list, timer_hour, timer_min, timer_sec, ment_string
	weather_list = weather_data_handler.weather_parsing()
	weather_list.append(weather_data_handler.dust_grade())
	timer_hour = timer.hour_slice()
	timer_min = timer.min_slice()
	timer_sec = timer.sec_slice()
	#ment_string = ment_handler.ment_return(weather_list) ment should be update in specific time
	#print(weather_list)

class Form:
	def __init__(self):
		self.mirror = Ui_MainWindow()
		self.app, self.MainWindow, self.ui = setup()
		self.mirror.setupUi(self.MainWindow)
		self.user = ''
		self.ment_method = [] 

	def start_ui(self):
		self.MainWindow.show()
		sys.exit(self.app.exec_())

	def update_info(self):
		while True:
			get_info()
			self.reset_init()
			self.image_select()
			time.sleep(5)

	def ment_lb_settext(self):
		self.mirror.setText("ment_lb_settext !!!!!!")
		return ""

	def update_speech(self):
		while True:
			self.mirror.ment_lb.setText("안녕하세요 세미입니다")
			activate_env_speech.activate()
			with open('/home/pi/smart_mirror/text_directory/speech_text.txt', 'r') as f:
				self.mic_text = f.read()

			if self.mic_text in '그만할래':
				self.MainWindow.close()
				break

			if self.mic_text in ment_json:
				for self.i in ment_json[self.mic_text]:
					self.ment_method = str_to_method(self.i)
					self.temp = self.ment_method()

			"""	
			if self.mic_text in '사용자등록':
				print(server.return_ip())
				self.ip, self.port = server.return_ip()
				server.server_start()
				self.class1.Hi.setText("ip : " + self.ip + "port : " + self.port)

			if self.mic_text in '그만할래':
				self.MainWindow.close()
				break
			if self.mic_text == '오늘나의할일은':
				self.user = self.mic_text
				reset_scheduler(self.user)
				self.schedule_reset()
			"""

	def image_select(self):
		global weather_list

		if weather_list[3] == 0:
			pass
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
			self.mirror.weather_icon_lb.setPixmap(QPixmap(pixmap))
		elif weather_list[3] == 3:
			pixmap = QPixmap("./picture/snow.png")
			self.mirror.weather_icon_lb.setPixmap(QPixmap(pixmap))
		elif weather_list[3] == 4:
			pixmap = QPixmap("./picture/rain.png")
			self.mirror.weather_icon_lb.setPixmap(QPixmap(pixmap))

	def schedule_reset(self):
		global scheduler_string
		self.mirror.schedule_tb.setText(scheduler_string)
	
	def reset_init(self):
		global timer_hour, timer_min, weather_list, timer_sec, ment_string
		self.mirror.time_lb.setText("  " + timer_hour + ":" + timer_min + ":" + timer_sec)
		self.mirror.wetness_lb.setText("  습도  " + str(weather_list[0]) + "%")
		self.mirror.temperature_lb.setText("  온도  " + str(weather_list[1]) + "°C")
		self.mirror.dust_lb.setText("미세먼지 " + str(weather_list[4])) 


t = Form()
updater = threading.Thread(target=t.update_info, args=())
updater.daemon = True
updater.start()

speech = threading.Thread(target=t.update_speech , args=())
speech.daemon = True
speech.start()


t.start_ui()

