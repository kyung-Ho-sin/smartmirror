from ui_object import t
import threading
import os, sys, json
from user_app.server import *
from caldavclient.schedule_handler import Handler_parse


def str_to_method(str):
	return getattr(sys.modules[__name__], str)

speech = threading.Thread(target=t.update_speech, args=(str_to_method,))
speech.daemon = True
speech.start()

updater = threading.Thread(target=t.update_info, args=())
updater.daemon = True
updater.start()


t.start_ui()

def show_schedule():
#	global t
	t.mirror.ment_lb.setText("비밀문장을 말해주세요")
	activate_env_speech.activate()
	t.mirror.ment_lb.setText("비밀문장 입력이 완성되었습니다")
	with open('/home/pi/smart_mirror/text_directory/speech_text.txt', 'r') as f:
		mic_text = f.read()
	has_func = hashlib.md5()
	has_func.update(mic_text)
	mic_text = has_func.hexdigest()
	with open('/home/pi/smart_mirror/text_directory/user_info.json') as x:
		user_info_json = json.load(x)
	if mic_text in user_info_json:
		user_info_list = user_info_json[mic_text]
	else:
		t.mirror.ment_lb.setText("비밀문장이 틀렸습니다")
		show_schedule()
#	user_schedule_list = Handler_parse.parseInfo(user_info_list[0], user_info_list[1])
	print("!!!!!")
#	print(user_schedule_list)
