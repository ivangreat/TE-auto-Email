import os
import re
import datetime
import time
import yagmail
import requests
import json
from requests.compat import urljoin
import base64

ip = ''
port = ''
h = 'http'

def login():
	base_url = f'{h}://{ip}:{port}/webapi/'
	auth_url = urljoin(base_url,'auth.cgi')
	auth_params = {
		'api': 'SYNO.API.Auth',
		'version': '3',
		'method': 'login',
		'account': '',
		'passwd': '',
		'session': 'FileStation',
		'format': 'cookie'
		}
	auth_api_url = requests.get(auth_url, params = auth_params).json()
	if auth_api_url['success']:
		token = auth_api_url['data']['sid']
	return token

sid = login()

def download(file_path):
	base_url = f'{h}://{ip}:{port}/webapi/'
	down_url = urljoin(base_url,'entry.cgi')
	auth_params = {
		'api': 'SYNO.FileStation.Download',
		'version': '2',
		'method': 'download',
		'path':	file_path,
		'mode': 'download'
		}
	auth_params['_sid'] = sid
	download_api_url = requests.get(down_url, params = auth_params)
	return download_api_url.url

def check_folder():
	li = []
	for root, dirs, file_name in os.walk(r'/volume1/KN FILE/Destination Documents/'):
		subfolder = re.findall(r'\w{4}\d{7}',root)
		for folder_name in subfolder:
			if folder_name in root:
				li.append(root)
	return li

def new_file():
	li2,li3 = [],[]
	for a in check_folder():
		b = os.listdir(a)
		for c in b:
			d = os.path.getmtime(os.path.join(a,c))
			if (time.time() - d <= 1800) and (len(b) == 3) and ((a.split("/")[-1]).split()[0] not in ["Mala","Dobra"]):
				li2.append(a)
			elif (time.time() - d <= 1800) and (len(b) == 2) and ((a.split("/")[-1]).split()[0] in ["Mala","Dobra","Budapest","D.S."]):
				li3.append(a)
	return list(set(li2 + li3))

def output():
	li4 = []
	for order_sq, f in enumerate(new_file(),1):
		e = "No.%(number)d\nTrain Number: %(name)s\nDestination document: <a href ='%(link)s'>%(path)s</a>\nDestination Station/Container Number: %(path1)s" % {"number":order_sq,"name":f.split("/")[-2],"path":", ".join([x for x in os.listdir(f)]),"path1":f.split("/")[-1],"link":download('/' + f.split("/",2)[-1])}
		li4.append(e)
	return li4

if len(output()) == 0:
	pass
else:
	li4 = [x for x in output()]
	y = ("\n" * 2).join(li4)
	mail = yagmail.SMTP(user = '',password = '', host = 'smtphz.qiye.163.com')
	attempts = 0
	success = False
	while attempts < 5 and not success:
		try:
			mail.send(
				to = [],
				cc = [],
				subject = f'New Destination Documents Added at BTE Website - Pre-alert - {time.strftime("%Y/%m/%d-%H:%M",time.localtime(time.time()))}',
				contents = """<html><body>
				Dear Colleagues,
				Please be advised some new destination documents are uploaded at BTE’s website for your further disposal.
							  <p>%s</p>					 
				</body></html>""" % y
				)
			mail.close()
			success = True
		except:
			time.sleep(10)
			attempts += 1
			if attempts == 5:
				raise Exception('Failed to send Email! Please check!')

