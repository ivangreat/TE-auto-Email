from PIL import Image
from aip import AipOcr
import re
import os
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape

class waybill_rec():
	f = open('箱号.txt')
	line = f.readlines()

	def __init__(self,name):
		self.name = name
		self.APP_ID = ''
		self.API_KEY = ''
		self.SECRET_KEY = ''
		
	def crop_image(self):
		self.im = Image.open(self.name)
		width,height = self.im.size
		self.box = (int(0.030 * width), int(0.500*height), int(0.300*width), int(0.700*height))
		self.region = self.im.crop(self.box)
		self.region.save(self.name[:-4] + '.jpeg')

	def baidu_ocr(self):
		self.client = AipOcr(self.APP_ID,self.API_KEY,self.SECRET_KEY)
		self.file = open(os.path.join(os.getcwd(),self.name[:-4] + '.jpeg'),'rb')
		self.img = self.file.read()
		time.sleep(0.5)
		self.message = self.client.basicGeneral(self.img)
		self.file.close()

	def recognition(self):
		for self.words_ocr in self.message.get('words_result'):
			self.ocr_list = re.findall(r'(?<=[Uu])[0-9]{7}(?!/\d)',self.words_ocr.get('words'))
			if "".join(self.ocr_list) =="":
				continue
			self.ocr_number = ''.join(self.ocr_list)

	
	def rename(self):
		for k in waybill_rec.line:
			if self.ocr_number == k[4:11]:
				os.rename(self.name, k[:11] + '.png')

	def start(self):
		self.crop_image()
		self.baidu_ocr()
		self.recognition()
		self.rename()


for pdffile in os.listdir():
	if pdffile.endswith('pdf'):
		command = r'F:\mupdf-1.18.0-windows\mutool.exe convert -o file%02d.png -O resolution=149.957 ' + pdffile
		os.system(command)

time.sleep(0.5)

for i in os.listdir():
	if i.endswith('png'):
		p = waybill_rec(i)
		p.start()

for x in os.listdir():
	if x.endswith('png'):
		im=Image.open(x)
		im_w,im_h=im.size
		newname=x[:x.rindex('.')]+'.pdf'
		c=canvas.Canvas(newname,pagesize=(im_w,im_h))
		c.drawImage(x,0,0,im_w,im_h)
		c.save()
		c.showPage()
		im.close()
		os.remove(x)
	elif x.endswith('jpeg'):
		os.remove(x)
