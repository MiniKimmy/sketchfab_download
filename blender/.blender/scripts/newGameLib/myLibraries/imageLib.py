import struct
import os
import Blender


def imageConvert(input):
	pvr=input.replace('.img','.pvr')
	if os.path.exists(input)==True:
		os.rename(input,pvr)
		exe=toolsDir+os.sep+"PVRTexToolCLI.exe"
		command=exe+' -i "'+pvr+'" -d -f r8g8b8a8'
		os.system(command)
	if os.path.exists(pvr)==True:
		exe=toolsDir+os.sep+"PVRTexToolCLI.exe"
		command=exe+' -i "'+pvr+'" -d -f r8g8b8a8'
		os.system(command)
	return pvr.replace('.pvr','.png')


def ddsheader():
	ddsheader = '\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x0A\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x05\x00\x00\x00\x44\x58\x54\x31\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	return ddsheader
   

def tga_16(data):
	newdata=''
	for m in range(len(data)/2):
		a=struct.unpack('H',data[m*2:m*2+2])[0]
		r = (a & 0xF800) >11
		g = (a & 0x07E0) >5
		b = (a & 0x001F)
		r = r * 255 / 31
		g = g * 255 / 63
		b = b * 255 / 31
		newdata+=struct.pack('iii',r,g,b)
		
	
	return newdata
		


def RGB565_2_RGB888(szer,wys,data,outname):
	newdata=''
	start=0
	image=Blender.Image.New(outname,szer,wys,24)
	for m in range(szer):
		for n in range(wys):
			c=struct.unpack('H',data[start:start+2])[0]
			start+=2
			r = (c>>11)&0x1f
			g = (c>>5)&0x3f
			b = c&0x001f  
	   		pr=(r<<3)|(r>>2)
			pg=(g<<2)|(g>>4)
			pb=(b<<3)|(b>>2)	
			if pr==0 and pg==0 and pb==0:
				pa=1
			else:
				pa=0		
			image.setPixelI(n, 511-m, (pr, pg, pb,pa))
			#newdata+=struct.pack('iii',pr,pg,pb)
	#return newdata
	image.save()	

def ARGB1555_2_ARGB8888(data):
	newdata=''
	for m in range(len(data)/2):
		c=struct.unpack('H',data[m*2:m*2+2])[0]
		a = c&0x8000
		r = c&0x7C00
		g = c&0x03E0
		b = c&0x1F
		rgb = (r << 9) | (g << 6) | (b << 3)
		integer=(a*0x1FE00) | rgb | ((rgb >> 5) & 0x070707)
		newdata+=struct.pack('I',integer)
	return newdata
		
			
class Obrazek():
	def __init__(self):
		self.format=None
		self.wys=None
		self.szer=None
		self.name=None
		self.data=None
	def save(self):
		if self.format is not None:
			if self.wys is not None:
				if self.szer is not None:
					if self.name is not None:
						if self.data is not None:
							if os.path.exists(Blender.sys.dirname(self.name))==False:
								os.makedirs(Blender.sys.dirname(self.name))
							if self.format=='DXT1':
								newfile=open(self.name,'wb')
								newfile.write(ddsheader())
								newfile.seek(0xC)
								newfile.write(struct.pack('i',self.wys))
								newfile.seek(0x10)
								newfile.write(struct.pack('i',self.szer))
								newfile.seek(0x54)
								newfile.write('DXT1')
								newfile.seek(128)
								newfile.write(self.data)
								newfile.close()
							elif self.format=='DXT3':
								newfile=open(self.name,'wb')
								newfile.write(ddsheader())
								newfile.seek(0xC)
								newfile.write(struct.pack('i',self.wys))
								newfile.seek(0x10)
								newfile.write(struct.pack('i',self.szer))
								newfile.seek(0x54)
								newfile.write('DXT3')
								newfile.seek(128)
								newfile.write(self.data)
								newfile.close()
							elif self.format=='DXT5':
								newfile=open(self.name,'wb')
								newfile.write(ddsheader())
								newfile.seek(0xC)
								newfile.write(struct.pack('i',self.wys))
								newfile.seek(0x10)
								newfile.write(struct.pack('i',self.szer))
								newfile.seek(0x54)
								newfile.write('DXT5')
								newfile.seek(128)
								newfile.write(self.data)
								newfile.close()
							elif self.format=='tga32':
								newfile=open(self.name,'wb')
								newfile.write('\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
								newfile.write(struct.pack('H',self.wys))
								newfile.write(struct.pack('H',self.szer))
								newfile.write('\x20\x20')
								newfile.write(self.data)
								newfile.close()
							elif self.format=='tga16':
								newfile=open(self.name,'wb')
								newfile.write('\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
								newfile.write(struct.pack('H',self.wys))
								newfile.write(struct.pack('H',self.szer))
								newfile.write('\x20\x20')
								newfile.write(tga_16(self.data))
								newfile.close()
							elif self.format=='tga24':
								newfile=open(self.name,'wb')
								newfile.write('\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
								newfile.write(struct.pack('H',self.wys))
								newfile.write(struct.pack('H',self.szer))
								newfile.write('\x18\x20')
								"""id=0
								for m in range(self.szer):
									for n in range(self.wys):
										data=self.data[id*3:id*3+3]
										newfile.write(data)
										newfile.write('\x00')
										id+=1"""
								newfile.write(self.data)
								#newfile.write(tga_16(self.data))
								newfile.close()
							elif self.format=='RGB2BGR':
								newfile=open(self.name,'wb')
								newfile.write('\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
								newfile.write(struct.pack('H',self.wys))
								newfile.write(struct.pack('H',self.szer))
								newfile.write('\x18\x20')
								id=0
								for m in range(self.szer):
									for n in range(self.wys):
										data=self.data[id*3:id*3+3][::-1]
										#data.reverse()
										newfile.write(data)
										id+=1
								newfile.close()
							elif self.format=='565to888':
								#newfile=open(self.name,'wb')
								#newfile.write('\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
								#newfile.write(struct.pack('H',self.wys))
								#newfile.write(struct.pack('H',self.szer))
								#newfile.write('\x20\x20')
								#newfile.write(
								RGB565_2_RGB888(self.szer,self.wys,self.data,self.name)
								#)
								#newfile.close()
							else:
								print 'WARNING: nieznany format',self.format
