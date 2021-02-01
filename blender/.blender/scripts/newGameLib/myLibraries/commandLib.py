import os
import Blender	
	
blendDir=os.path.dirname(Blender.Get('filename'))
toolsDir=blendDir+os.sep+"newGameLib"+os.sep+"tools"


									
class Cmd:
	def __init__(self):
		self.type=None
		self.input=None
		self.output=None
		self.option=None
		self.exe=None
		self.line=None
		self.script=None
		
	def OFFZIP(self):	
		self.option='-a -1'
		self.start='0'
		self.exe=toolsDir+os.sep+"Offzip"+os.sep+"offzip.exe"
		self.line=self.exe+' '+self.option+'  "'+self.input+'" "'+self.output+'" "'+self.start+'"'
		os.system(self.line)
		
	def PNG(self):	
		self.option=' -out png '
		self.exe=toolsDir+os.sep+"Nconvert/nconvert.exe"	
		self.line=self.exe+self.option+' "'+ self.input+'"'	
		os.system(self.line)
		
	def JPG(self):	
		self.option=' -out jpeg '
		self.exe=toolsDir+os.sep+"Nconvert/nconvert.exe"	
		self.line=self.exe+self.option+' "'+ self.input+'"'	
		os.system(self.line)
		
	def GR2(self):	
		self.option='-a'
		self.exe=toolsDir+os.sep+"Gr2/grnreader98.exe"
		self.line=self.exe+' "'+ self.input +'" '+ self.option
		os.system(self.line)
	
		
	def NOESIS(self):	
		self.option="?cmode"
		self.exe=toolsDir+os.sep+"noesis"+os.sep+"noesis.exe"
		self.line=self.exe+' "'+ self.input +'" '+ self.option
		os.system(self.line)
		
	def ZIP(self):	
		self.option='x'
		self.exe=toolsDir+os.sep+"7z"+os.sep+"7z.exe"
		self.line=self.exe+' '+self.option+' "'+self.input+'" -y -o"'+os.path.dirname(self.input)+'"'
		os.system(self.line)
		
	def CD(self):	
		self.exe=blendDir+os.sep+'"tools/CDisplay/CDisplay.exe"'
		self.line=self.exe+' "'+ self.input +'" '
		os.system(self.line)	
		
	def PDF(self):	
		self.exe=blendDir+os.sep+'"tools/PdfReader/reader.exe"'
		self.line=self.exe+' "'+ self.input +'" '
		os.system(self.line)
		
	def QUICKBMS(self):	
		self.option='"-export" "-meshes" "-nostat"'
		self.exe=toolsDir+os.sep+"quickbms"+os.sep+"quickbms.exe"
		self.script=toolsDir+os.sep+"quickbms"+os.sep+"bms"+os.sep+bms
		self.line=self.exe+self.script+self.input+self.output
		os.system(self.line)
		
	def UMODEL(self):	
		self.option='"-export" "-meshes" "-nostat"'
		self.exe=toolsDir+os.sep+'Umodel'+os.sep+'umodel.exe'
		self.line=self.exe+self.option
		os.system(self.line)
		
	def PVR(self):	
		self.option=' -i "'+self.input+'" -d -f r8g8b8a8'
		self.exe=toolsDir+os.sep+"Pvr"+os.sep+"PVRTexToolCLI.exe"
		self.line=self.exe+self.option
		os.system(self.line)
	
def do(filename):	
	cmd=Cmd()
	cmd.input=filename
	cmd.PVR()	

#Blender.Window.FileSelector(do)
		
		
		
		
		
		
		
		
		
		
		
			