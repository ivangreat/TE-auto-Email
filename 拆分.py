import pandas as pd
import os
from PyPDF2 import PdfFileWriter,PdfFileReader

list1 = []
for file in os.listdir():
	if file.endswith('xls'):
		data = pd.read_excel(file,sheet_name=0)
		data1 = data.iloc[:,1]
		for filename in data1.values:
			list1.append(filename)

for pdffile in os.listdir():
	if pdffile.endswith('pdf'):
		inputpdf = PdfFileReader(open(pdffile, "rb"))
		for i in range(inputpdf.numPages):
		    output = PdfFileWriter()
		    if i % 2 == 0:
			    output.addPage(inputpdf.getPage(i))
			    output.addPage(inputpdf.getPage(i+1))
			    with open("拆分第%s部分.pdf" % (i//2+1), "wb") as outputStream:
			        output.write(outputStream)
			        outputStream.close()
			        os.rename("拆分第%s部分.pdf" % (i//2+1),str(list1[(i//2)]) + ".pdf")
