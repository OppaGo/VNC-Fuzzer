from collections import namedtuple
from os import urandom
from random import randint
import socket

'''
ENCODING TYPE
+--------+-----------------------------+
| Number | Name                        |
+--------+-----------------------------+
| 0      | Raw                         |
| 1      | CopyRect                    |
| 2      | RRE                         |
| 5      | Hextile                     |
| 15     | TRLE                        |
| 16     | ZRLE                        |
| -239   | Cursor pseudo-encoding      |
| -223   | DesktopSize pseudo-encoding |
+--------+-----------------------------+
'''

class FramebufferParameter:

	def __init__(self):
		self.fieldname =[
		'Framebuffer width',\
		'Framebuffer height',\
		'Bits per pixel',\
		'Depth',\
		'Big endian flag',\
		'True color flag',\
		'Red maximum',\
		'Green maximum',\
		'Blue maximum',\
		'Red shift',\
		'Green shift',\
		'Blue shift',\
		'padding',\
		'Desktop Name Length',\
		'Desktop Name'\
		]

	def FbPrandom(self):
		data = dict()
		size1 = [2,3,4,5,9,10,11]
		size2 = [0,1,6,7,8]

		for i in size1:
			data[self.fieldname[i]] = urandom(1)
		for i in size2:
			data[self.fieldname[i]] = urandom(2)

		data[self.fieldname[12]] = urandom(3) # padd
		data[self.fieldname[13]] = urandom(4) # size
		data[self.fieldname[14]] = urandom(randint(0,3000))

		self.data = data
		return data

	def FuzzData(self):
		data = ''
		ran = self.FbPrandom()

		for i in range(len(ran)):
			data += ran[self.fieldname[i]]

		return data

	def savelog(self,name):
		f = open('./log/' + name,'w')

		f.write('=================== LOG ===================\n')
		f.write('Protocol : RFB_FramebufferParameter \n')

		for i in range(len(self.fieldname)):
			logd = self.fieldname[i] + " : "
			logd += self.data[self.fieldname[i]].encode('hex') + "\n"

			f.write(logd)

		f.close()

class FramebufferUpdate:

	def __init__(self):
		self.fieldname =[
		'message-type',\
		'padding',\
		'number-of-rectangles',\
		'x-position',\
		'y-position',\
		'width',\
		'height',\
		'encoding-type',\
		'data'\
		]

		self.encodingtype =\
		['\x00\x00\x00\x00',\
		'\x01\x00\x00\x00',\
		'\x02\x00\x00\x00',\
		'\x05\x00\x00\x00',\
		'\x15\x00\x00\x00',\
		'\x16\x00\x00\x00',\
		'\x11\xff\xff\xff',\
		'\x21\xff\xff\xff']

	def FbUrandom(self):
		data = dict()

		size1 = [1]
		size2 = [3,4,5,6]

		data[self.fieldname[0]] = '\x00'
		data[self.fieldname[2]] = '\x01\x00'

		for i in size1:
			data[self.fieldname[i]] = urandom(1)

		for i in size2:
			data[self.fieldname[i]] = urandom(2)

		data[self.fieldname[7]] = self.encodingtype[randint(0,7)]
		data[self.fieldname[8]] = urandom(randint(0,3000))

		self.data = data

		return data

	def FuzzData(self):
		data = ''
		ran = self.FbUrandom()

		for i in range(len(ran)):
			data += ran[self.fieldname[i]]
		return data

	def savelog(self,name):
		f = open('./log/' + name,'w')

		f.write('=================== LOG ===================\n')
		f.write('Protocol : RFB_FramebufferUpdate \n')

		for i in range(len(self.fieldname)):
			logd = self.fieldname[i] + " : "
			logd += self.data[self.fieldname[i]].encode('hex') + "\n"

			f.write(logd)

		f.close()

class SetColorMapEntries:

	def __init__(self):
		self.fieldname =[
		'message-type',\
		'padding',\
		'first-color',\
		'number-of-colors',\
		'red',\
		'green',\
		'blue',\
		]

	def SCMErandom(self):
		data = dict()

		size1 = [1]
		size2 = [2,3,4,5,6]

		data[self.fieldname[0]] = '\x01'

		for i in size1:
			data[self.fieldname[i]] = urandom(1)

		for i in size2:
			data[self.fieldname[i]] = urandom(2)

		self.data = data

		return data

	def FuzzData(self):
		data = ''
		ran = self.SCMErandom()

		for i in range(len(ran)):
			data += ran[self.fieldname[i]]
		return data

	def savelog(self,name):
		f = open('./log/' + name,'w')

		f.write('=================== LOG ===================\n')
		f.write('Protocol : RFB_SetColorMapEntries \n')

		for i in range(len(self.fieldname)):
			logd = self.fieldname[i] + " : "
			logd += self.data[self.fieldname[i]].encode('hex') + "\n"

			f.write(logd)

		f.close()

class ServerCutText:

	def __init__(self):
		self.fieldname =[
		'message-type',\
		'padding',\
		'length',\
		'text',\
		]

	def SCTrandom(self):
		data = dict()

		data[self.fieldname[0]] = '\x03'
		data[self.fieldname[1]] = urandom(3)
		data[self.fieldname[2]] = urandom(4)
		data[self.fieldname[3]] = urandom(randint(0,60535))

		self.data = data

		return data

	def FuzzData(self):
		data = ''
		ran = self.SCTrandom()

		for i in range(len(ran)):
			data += ran[self.fieldname[i]]
		return data

	def savelog(self,name):
		f = open('./log/' + name,'w')

		f.write('=================== LOG ===================\n')
		f.write('Protocol : RFB_ServerCutText \n')

		for i in range(len(self.fieldname)):
			logd = self.fieldname[i] + " : "
			logd += self.data[self.fieldname[i]].encode('hex') + "\n"

			f.write(logd)

		f.close()

class RandomData:

	def __init__(self):
		self.fieldname =[
		'random',\
		]

	def Rrandom(self):
		data = dict()

		data[self.fieldname[0]] = urandom(randint(0,60535))

		self.data = data

		return data

	def FuzzData(self):
		data = ''
		ran = self.Rrandom()

		for i in range(len(ran)):
			data += ran[self.fieldname[i]]
		return data

	def savelog(self,name):
		f = open('./log/' + name,'w')

		f.write('=================== LOG ===================\n')
		f.write('Protocol : RandomData \n')

		for i in range(len(self.fieldname)):
			logd = self.fieldname[i] + " : "
			logd += self.data[self.fieldname[i]].encode('hex') + "\n"

			f.write(logd)

		f.close()

'''
class Fuzz()

coding~~

'''

def main():

	a = RandomData()
	a.FuzzData()
	print a.FuzzData()
	print a.savelog('log5')


if __name__ == "__main__":
	main()
