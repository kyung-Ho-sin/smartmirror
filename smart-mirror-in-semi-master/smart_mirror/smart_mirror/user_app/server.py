# -*- coding: utf-8 -*-
import hashlib    # MD5를 구하기 위해 import
import netifaces as ni
import re
import socket
import json
import os
from collections import OrderedDict
import sys
sys.path.insert(0, '/home/pi/samrt_mirror/')
from ui_object import t
from caldavclient.caldavclient import CaldavClient

def do_some_stuffs_with_input(input_string):
	#통신시 받을 내용 줄바꿈해서 저장
	list_u = input_string.split('\n')
	
	return list_u

def hashing_passphrase(passphras):
	pattern = re.compile(r'\s+') #공백(space) 패턴 객체화
	passphras = re.sub(pattern, '', passphras) #패턴 객체화된 공백을 ''로 바꿈 -> 띄어쓰기 제거
	print(passphras)# 공백 제거 확인 위함(삭제필요)
	passphras=passphras.encode("utf8")#utf8로 인코딩
	has_func = hashlib.md5()    # MD5 hash function
	has_func.update(passphras)   # hashing!
	passphras=has_func.hexdigest()# 메시지 다이제스트를 얻음(16진수 해시값)
	print(has_func.hexdigest())
	return passphras

def new_user(n_pwp, n_uid, n_upw):
	global t
	t.mirror.ment_lb.setText("신규 사용자 정보 입력") 
	n_pwp=hashing_passphrase(n_pwp)
	if CaldavClient("https://caldav.calendar.naver.com/principals/",(n_uid, n_upw)) != None:
		if os.path.exists('/home/pi/smart_mirror/text_directory/user_info.json') :         #처음 구동시 DB.TXT있는지 유무확인후 없으면 생성 필요
			with open('/home/pi/smart_mirror/text_directory/user_info.json') as data_file:    #파일이 존재하면 값을 읽어옴
				dict = json.load(data_file) #해당 .json 의 값을 dict에 읽어들임
			t.mirror.ment_lb.setText("'.json' load")
			if dict.get(n_pwp):
				t.mirror.ment_lb.setText("이미 존재하는 패스 프레이즈 입니다.")
				return 1
			else:
				dict[n_pwp] = [n_uid, n_upw] #새롭게 추가된 값 dict에 추가

		else : #.json파일 존재 안하면
			dict={n_pwp:[n_uid, n_upw]}#새롭게 추가된 값 dict에 추가
		print(dict)#dict 안에 저장된 값 확인위해(삭제필요)
		with open('/home/pi/smart_mirror/text_directory/user_info.json','w',encoding='utf-8')as make_file: #.json파일 쓰기형식, utf-8 로 인코딩해 오픈
			json.dump(dict, make_file, ensure_ascii=False, indent="\t")    #dict의 값을 .json에 씀
		return 0
	else :
		return 5

def exist_user(e_pwp, e_del_pwp, e_uid, e_upw):
	global t
	t.mirror.ment_lb.setText("기존 사용자 정보 변경")
	e_pwp=hashing_passphrase(e_pwp)
	e_del_pwp=hashing_passphrase(e_del_pwp)

	if CaldavClient("https://caldav.calendar.naver.com/principals/",(n_uid, n_upw)) != None:
		if os.path.exists('/home/pi/smart_mirror/text_directory/user_info.json') :         #처음 구동시 DB.TXT있는지 유무확인후 없으면 생성 필요
			with open('/home/pi/smart_mirror/text_directory/user_info.json') as data_file:    #파일이 존재하면 값을 읽어옴
				dict = json.load(data_file) #해당 .json 의 값을 dict에 읽어들임
			t.mirror.ment_lb.setText("'.json' load")
			compare_Uinfo=dict.get(e_del_pwp)
			if(compare_Uinfo==[e_uid, e_upw]):
				if dict.get(e_del_pwp):
					t.mirror.ment_lb.setText("이전 기록 삭제")
					del dict[e_del_pwp]
					t.mirror.ment_lb.setText("사용자 정보 수정")
					dict[e_pwp] = [e_uid, e_upw]
				else:
					return 3 #기존 패스프레이즈 잘못입	

			else:
				return 3
		else : #.json파일 존재 안하면
			t.mirror.ment_lb.setText("신규 json 파일 생성")
			dict={e_pwp:[e_uid, e_upw]}#새롭게 추가된 값 dict에 추가
		print(dict)#dict 안에 저장된 값 확인위해(삭제필요)
		with open('/home/pi/smart_mirror/text_directory/user_info.json','w',encoding='utf-8')as make_file: #.json파일 쓰기형식, utf-8 로 인코딩해 오픈
			json.dump(dict, make_file, ensure_ascii=False, indent="\t")    #dict의 값을 .json에 씀
		return 4
	else :
		return 5

def data_Processing(r_data):
	global t
	for n in range(len(r_data)):
		if n%5==0:
			d_info=r_data[n]
		if n%5==1:
			d_pwp=r_data[n]
		if n%5==2:
			d_del_pwp=r_data[n]
		if n%5==3:
			d_uid=r_data[n]
		if n%5==4:
			d_upw=r_data[n]
	t.mirror.ment_lb.setText("data_Processing Complite")
	return d_info, d_pwp, d_del_pwp, d_uid, d_upw

def error_messge(error_num, er_pwp, er_uid, er_upw):
	if error_num == 0:
		e_message="사용자의 정보가 성공적으로\n등록 되었습니다."
		sand_client=b'\n pwp : '+er_pwp.encode()+b'\n id : '+er_uid.encode()+b'\n pw : '+er_upw.encode()+b'\n\n'+e_message.encode()
	elif error_num == 1:
		e_message="\n동일한 패스프레이즈가 존재합니다.\n새로운 패스프레이즈를 입력하세요"
		sand_client=e_message.encode()
	elif error_num == 3:
		e_message="\n입력된 ID,PW 또는 변경할 문장이\n기존 정보와 다릅니다.\n다시 입력해 주세요."
		sand_client=e_message.encode()	
	elif error_num == 4:
		e_message="사용자 정보가 성공적으로\n변경 되었습니다."
		sand_client=b'\n pwp : '+er_pwp.encode()+b'\n id : '+er_uid.encode()+b'\n pw : '+er_upw.encode()+b'\n\n'+e_message.encode()
	elif errer_num == 5:
		e_message="\n입력하신 ID,PW 가 잘못된 정보입니다.\n올바른 id, pw를 입력해 주세요."
		sand_client=e_message.encode()
	else:
		e_message="치명적인 오류 발생\n어플리케이션의 재부팅이\n필요합니다."
		sand_client=e_message.encode()
	return sand_client

def server_start():
	global t
	verify=0
	ni.ifaddresses('wlan0') #wlan0
	HOST = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
	PORT = 9999
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	t.mirror.ment_lb.setText ("IPAddres is = " + HOST + "\nPORT is =" + str(PORT))
	s.bind((HOST,PORT))
	s.listen(1)
	
	checker = True
	
	while checker:
		conn, addr = s.accept()
		print("Connected by ", addr)
		#데이터 수신
		data = conn.recv(1024) # 소켓에서 (bufsize) 만큼 데이터를 수신
		data = data.decode("utf8").strip()
		if not data: break
		# 수신한 데이터저장
		res = do_some_stuffs_with_input(data)
		t.mirror.ment_lb.setText("Received: \n")
		#클라이언트에게 답을 보냄
		einfo, pwp, del_pwp, uid, upw = data_Processing(res)  
		
		if einfo == '0':
			verify  = new_user(pwp, uid, upw)
		elif einfo == '1':
			verify = exist_user(pwp, del_pwp, uid, upw)
		else:
			conn.sendall(error_messge(9, pwp, uid, upw).encode())
			conn.close()
			break

		conn.sendall(error_messge(verify, pwp, uid, upw))

		if verify == 0 or verify == 4:
			checker = False

		conn.close()
	
	t.mirror.ment_lb.setText("connect closed")
	
		#연결 닫기
	s.close()


