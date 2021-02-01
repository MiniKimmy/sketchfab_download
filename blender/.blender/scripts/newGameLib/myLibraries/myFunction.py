import bpy
import Blender,os	
from Blender.Mathutils import *
import types
from Blender.Draw import *
import math
from math import *


def setBoneMatrix(object,skeletonObject,boneName):
	bones=skeletonObject.getData().bones
	if boneName in bones.keys():
		matrix=bones[boneName].matrix['ARMATURESPACE']
		object.setMatrix(matrix)

def removeMaterials():
		scn = data.scenes.active
		for ob in scn.objects.context:
				if not ob.lib and ob.type == 'Mesh':    # object isn't from a library and is a mesh
 
						me = ob.getData(mesh=1)	
						nme=NMesh.GetRaw(me.name)
						mats = nme.materials 
						i=0
						for m in mats:
								del nme.materials[i]
								i += 1
								nme.update()
						print mats

"""


def XOR(inData,key):
	outData=''
	for val in inData:
		outData+=chr(ord(val)^0x96)
	return outData	


byte=0x2
byte = bin(byte)[2:].rjust(8, '0')
print byte
"""

"""

				for fc in msh.faces:
					fc.mode |= Blender.NMesh.FaceModes['TEX']
					fc.mode |= Blender.NMesh.FaceModes['LIGHT']
					
				if len(newdoubles) > 0:
					f.mode |= Blender.NMesh.FaceModes['TWOSIDE']  
					
            nrot = doc.createElement("rotate")
            nrot.setAttribute("x", "1")
            nrot.setAttribute("angle", str(180/3.1416*obj.rotation_euler[0]))
            ntrans.appendChild(nrot)
            nrot = doc.createElement("rotate")
            nrot.setAttribute("y", "1")
            nrot.setAttribute("angle", str(180/3.1416*obj.rotation_euler[1]))
            ntrans.appendChild(nrot)
            nrot = doc.createElement("rotate")
            nrot.setAttribute("z", "1")
            nrot.setAttribute("angle", str(180/3.1416*obj.rotation_euler[2]))
            ntrans.appendChild(nrot)
            nmove = doc.createElement("translate")
            nmove.setAttribute("x", '%3.3f' % obj.location.x)
            nmove.setAttribute("y", '%3.3f' % obj.location.y)
            nmove.setAttribute("z", '%3.3f' % obj.location.z)
			
			
			
			
			euler = Blender.Mathutils.Euler()
			RotateEuler(euler,z,'z')
			RotateEuler(euler,x,'x')
			RotateEuler(euler,y,'y')
			matrix=euler.toMatrix().resize4x4()
"""



#	t = Blender.sys.time()
#	print '%.2f seconds' % (Blender.sys.time()-t) 





 #       material.setMode(Blender.Material.Modes.TEXFACE + Blender.Material.Modes.TEXFACE_ALPHA)
#
 #       face.uv = [vertex.uvco for vertex in face_vertices]
#
#            for face in mesh.faces:
#                face.mode = Blender.Mesh.FaceModes.TEX + Blender.Mesh.FaceModes.TWOSIDE
#                face.image = image

"""
    try:
        file_object = open(file_path, 'rb')
    except IOError, (errno, strerror):
        Blender.Draw.PupMenu("Error%%t|I/O error(%d): %s." % (errno, strerror))
    except Exception, err:
        Blender.Draw.PupMenu("Error%%t|.%s" % err)
    finally:
        if file_object is not None:
            file_object.close()
			
			
def main():
    def pw_file_selector(file_path):
        if file_path and not Blender.sys.exists(file_path):
            Blender.Draw.PupMenu("Error%%t|The file %s does not exist." % file_path)
        else:
            pw_ski_read(file_path)
    
    Blender.Window.FileSelector(pw_file_selector, 'Ok', Blender.sys.makename(ext='.ski'))


if __name__ == "__main__":
    main()



def EncString(string):
	enc = sys.getfilesystemencoding()
	
	return unicode(string,"shift-jis").encode(enc,"replace")			
	
def read_int(self, size):
        if size==1:
            return self.unpack("b", size)
        if size==2:
            return self.unpack("h", size)
        if size==4:
            return self.unpack("i", size)
        print("not reach here")
        raise ParseException("invalid int size: "+size)		
"""


#	model_name = model_name.decode('shift_jis').encode('UTF-8')





blendDir=os.path.dirname(Blender.Get('filename'))
toolDir=None
if os.path.exists(blendDir+os.sep+'tools')==True:
	toolDir=blendDir+os.sep+'tools'
elif os.path.exists(blendDir+os.sep+'newgameLib/tools')==True:
	toolDir=blendDir+os.sep+'newgameLib/tools'

class switch(object):
	def __init__(self, value):
		self.value = value
		self.fall = False

	def __iter__(self):
		"""Return the match method once, then stop"""
		yield self.match
		raise StopIteration
    
	def match(self, *args):
		"""Indicate whether or not to enter a case suite"""
		if self.fall or not args:
			return True
		elif self.value in args: # changed for v1.5, see below
			self.fall = True
			return True
		else:
			return False

	
#a=range(5)
#a=[0,1,2,3,4]
#print a[::-1]
#a=[5,4,3,2,1]	



#			perm=itertools.permutations([0,1,2,3],4)

"""
def read(filename):
    time1 = time.time()
    path = os.path.dirname(filename)
    os.chdir(path)
    print path
    os.system("cls") if "nt" in os.name else os.system("clear")
    if zipfile.is_zipfile(filename):
        zf = zipfile.ZipFile(filename, "r")
        print zf
        for m in range(len(zf.namelist())):
            member = zf.namelist()[m]
            print member
            filename = zf.open(member)
            #print "Unzipping", member
            try:load_meshes(filename)
            except:pass 
            Blender.Window.Redraw()
    time2 = time.time()
    print "Total import time is: %.2f seconds." % (time2 - time1)
"""	
	
"""

			euler = Blender.Mathutils.Euler()
			RotateEuler(euler,z,'z')
			RotateEuler(euler,x,'x')
			RotateEuler(euler,y,'y')
			matrix=euler.toMatrix().resize4x4()
			bone.rotKeyList.append(matrix)
"""

	
	
def write(input,list,pad):
	string=' '*pad
	for item in list:
		string+=str(item)+' '
	string+='\n'
	input.write(string)	
	
	
def safe(count):
	if count<1000000:
		return range(count)
	else:
		print 'WARNING:too long:',count
		return [0]
	
	
"""	
def write(input,list,pad):
	if log==True:
		string=' '*pad
		for item in list:
			itemName=getNameVariable(item)
			if itemName is not None:
				string+=itemName+':'+str(item)+' '
			else:	
				string+=str(item)+' '
		string+='\n'
		input.write(string)	
	
def getNameVariable(variable):
	ID=eval("'" + str(id(variable)) + "'")
	output=None
	for name in dir():
		if id(eval(name))==ID:
			output=name
	return output		
"""	
"""	
	jj = 123
ID=eval("'" + str(id(jj)) + "'")
d=10
for x in dir():
	#print x	
	if id(eval(x)) ==ID:
		print x  
		
"""
"""
string.zfill()
"""		


"""
		byteAsInt=g.B(1)[0]
		ctrlBits.extend(map(int,list(bin(byteAsInt)[2:].rjust(8, '0'))))
"""		
	

	
	
class Input(object):
	def __init__(self,flagList):
		self.flagList=flagList
		self.type=None
		self.debug=None
		self.imageList=[]
		if type(flagList)==types.InstanceType:
			self.type='instance'
			self.filename=flagList.assetPath
			self.output=flagList
			self.returnList=self.flagList.returnList
			self.returnKey=self.flagList.returnKey
		if type(flagList)==types.StringType:
			self.type='string'
			self.filename=flagList
			
def Input1(object):
	return object	
			
def Output(object):	
	return object
			
		

def Float255(data):
	list=[]
	for get in data:
		list.append(get/255.0)
	return list	


def pm(message,n):
	print ' '*4*n,message

	
	
if toolDir is not None:	
	bmsDir=toolDir+os.sep+'quickbms'
	bmsExe=bmsDir+os.sep+'quickbms.exe'
	bmsScriptDir=bmsDir+os.sep+'scripts'
	
class Bms(object):
	def __init__(self):
		self.input=input
		self.output=''
		self.bms=None
		self.command=' '#' -d -o '
		
	def run(self):
		if self.bms is not None:
			self.bms=bmsScriptDir+os.sep+self.bms
			commandline = bmsExe +self.command+self.bms+ ' ' + self.input + ' '+self.output
			print commandline
			os.system(commandline)
			
		
class Searcher():
	def __init__(self):
		self.dir=None
		self.list=[]
		self.part=None#ext,dir,base
		self.what=None
	def run(self):
		dir=self.dir	
		def tree(dir):
			listDir = os.listdir(dir)
			olddir = dir
			for file in listDir:
				if self.part=='ext':
					if self.what.lower() in file.lower().split('.')[-1]:				
						if os.path.isfile(olddir+os.sep+file)==True:
							self.list.append(olddir+os.sep+file)
							
				else:			
					if self.what.lower() in file.lower():				
						if os.path.isfile(olddir+os.sep+file)==True:
							self.list.append(olddir+os.sep+file)
						
				if os.path.isdir(olddir+os.sep+file)==True:
					dir = olddir+os.sep+file
					tree(dir)
		tree(dir)	
		

		
	
	
def isQuat(quat):
	sum=quat[0]**2+quat[1]**2+quat[2]**2+quat[3]**2
	return sum	
	
	
	
def quatDecompress3(s0,s1,s2):  
	tmp0= s0>>15 
	tmp1= (s1*2+tmp0) & 0x7FFF
	s0= s0 & 0x7FFF ;
	tmp2= s2*4 ;
	tmp2= (s2*4+ (s1>>14)) & 0x7FFF ;
	s1= tmp1 ;
	AxisFlag= s2>>13 ;
	#AxisFlag = ((s1 & 1) << 1) | (s2 & 1)
	s2= tmp2 ;
	f0 = 1.41421*(s0-0x3FFF)/0x7FFF ;
	f1 = 1.41421*(s1-0x3FFF)/0x7FFF ;
	f2 = 1.41421*(s2-0x3FFF)/0x7FFF ;  
	f3 = sqrt(1.0-(f0*f0+f1*f1+f2*f2)) 
	#print AxisFlag
	if AxisFlag==3:
		x= f2
		y= f1
		z= f0
		w= f3
	if AxisFlag==2:x= f2;y= f1;z= f3;w= f0
	if AxisFlag==1:x= f2;y= f3;z= f1;w= f0
	if AxisFlag==0:x= f3;y= f2;z= f1;w= f0
	#print x,y,z,w  
	return x,y,z,w  

	
	
def quatDecompress(s0,s1,s2):  
	tmp0= s0>>15 
	tmp1= (s1*2+tmp0) & 0x7FFF
	s0= s0 & 0x7FFF ;
	tmp2= s2*4 ;
	tmp2= (s2*4+ (s1>>14)) & 0x7FFF ;
	s1= tmp1 ;
	AxisFlag= s2>>13 ;
	#AxisFlag = ((s1 & 1) << 1) | (s2 & 1)
	s2= tmp2 ;
	f0 = 1.41421*(s0-0x3FFF)/0x7FFF ;
	f1 = 1.41421*(s1-0x3FFF)/0x7FFF ;
	f2 = 1.41421*(s2-0x3FFF)/0x7FFF ;  
	f3 = sqrt(1.0-(f0*f0+f1*f1+f2*f2)) 
	#print AxisFlag
	if AxisFlag==3:
		x= f2
		y= f1
		z= f0
		w= f3
	if AxisFlag==2:x= f2;y= f1;z= f3;w= f0
	if AxisFlag==1:x= f2;y= f3;z= f1;w= f0
	if AxisFlag==0:x= f3;y= f2;z= f1;w= f0
	#print x,y,z,w  
	return x,y,z,w  
	
def QuatMatrix(quat):
	return Quaternion(quat[3],quat[0],quat[1],quat[2]).toMatrix()	
	
	
def VectorMatrix(vector):
	return TranslationMatrix(Vector(vector))		
	
	
def roundVector(vec,dec=17):
	fvec=[]
	for v in vec:
		fvec.append(round(v,dec))
	return Vector(fvec)
	
	
def roundMatrix(mat,dec=17):
	fmat = []
	for row in mat:
		fmat.append(roundVector(row,dec))
	return Matrix(*fmat)

def Matrix4x4(data):
	return Matrix(  data[:4],\
					data[4:8],\
					data[8:12],\
					data[12:16])	

def Matrix3x3(data):
	return Matrix(  data[:3],\
					data[3:6],\
					data[6:9])
	
	
def Matrix4x3(data):
	#print data
	data=list(data)
	return Matrix(  data[:3]+[0.0],\
					data[3:6]+[0.0],\
					data[6:9]+[0.0],\
					data[9:12]+[1.0])
		

def VectorScaleMatrix(scale):
	mat = Blender.Mathutils.Matrix(
			[1, 0, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1],
			)
	mat *= Blender.Mathutils.ScaleMatrix(scale[0], 4, Blender.Mathutils.Vector([1, 0, 0]))
	mat *= Blender.Mathutils.ScaleMatrix(scale[1], 4, Blender.Mathutils.Vector([0, 1, 0]))
	mat *= Blender.Mathutils.ScaleMatrix(scale[2], 4, Blender.Mathutils.Vector([0, 0, 1]))	
	return mat
	
	
def decrypt_string(string):
	'''Return the decrypted string. XOR each character in the string by
	FF to get the actual character. Strings are null-terminated.'''
	#string =B(count )
	inverted = ""
	print len(string)
	#for m in range(len(string)-1):
	for m in string:
		#pass
		#inverted += chr(string[i] ^ 0xFF)
		inverted += chr(m ^ 0x55)
	return inverted
	
class Script:
	"""
	init
		self.input=None
		self.VISUALISER=False
	object
		run()
	"""
	def __init__(self):
		self.input=None
		self.VISUALISER=False
		self.TEATIMEDECODER=False
	def run(self):
		if self.VISUALISER==True:
			textList=[]
			for text in Blender.Text.Get():
				if text.name not in textList:
					textList.append(text.name)
			scn = Blender.Scene.GetCurrent()
			self.input="libraryList\\visualiser.py"
			txt=Blender.sys.basename(self.input)
			if txt not in textList:
				text=Blender.Text.Load(self.input)
			scn.addScriptLink(txt,'Redraw')			
				

	
		
		
def ParseID():
		#0-0-0 - oznacza kolejno meshID - matID - objectID
		ids = []
		objectID=0
		modelID=0
		matID=0
		scene = bpy.data.scenes.active
		
		#for meshID
		for object in scene.objects:
			if object.getType()=='Mesh':
				try:
					meshID = int(object.getData(mesh=1).name.split('-')[0])
					ids.append(meshID)
				except:pass 
		try:
			meshID = max(ids)+1
		except:
			meshID = 0
		return meshID


class SceneIDList:
	def __init__(self):
		meshIDList=[]
		objectIDList=[]
		szkieletIDList=[]
		scene = bpy.data.scenes.active
		for object in scene.objects:
			if object.getType()=='Mesh':
				try:
					meshID = int(object.getData(mesh=1).name.split('-')[0])
					meshIDList.append(meshID)
				except:pass 
				try:
					objectID = int(object.getData(mesh=1).name.split('-')[2])
					objectIDList.append(objectID)
				except:pass 
		for mesh in bpy.data.meshes:
				try:
					objectID = int(mesh.name.split('-')[2])
					objectIDList.append(objectID)
				except:pass   
		for mesh in bpy.data.armatures:
				try:
					ID = int(mesh.name.split('-')[1])
					szkieletIDList.append(ID)
				except:pass   
		try:
			self.meshID = max(meshIDList)+1
		except:
			self.meshID = 0
		try:
			self.objectID = max(objectIDList)+1
		except:
			self.objectID = 0
		try:
			self.szkieletID = max(szkieletIDList)+1
		except:
			self.szkieletID = 0
		scene.update()	
			
		
		
		
		
FLT_EPSILON=0
def quatDecompress1(s0,s1,s2):

	which = ((s1 & 1) << 1) | (s2 & 1);
	s1 &= 0xfffe;
	s2 &= 0xfffe;

	scale = 1.0/32767.0/1.41421

	if which == 3:
		x = s0 * scale
		y = s1 * scale
		z = s2 * scale

		w = 1 - (x*x) - (y*y) - (z*z);
		if (w > FLT_EPSILON):
			w = sqrt(w);
	elif (which == 2):# {
		x = s0 * scale;
		y = s1 * scale;
		w = s2 * scale;

		z = 1 - (x*x) - (y*y) - (w*w);
		if (z > FLT_EPSILON):
			z = sqrt(z);
	elif (which == 1):# {
		x = s0 * scale;
		z = s1 * scale;
		w = s2 * scale;

		y = 1 - (x*x) - (z*z) - (w*w);
		if (y > FLT_EPSILON):
			y = sqrt(y);
	else:
		y = s0 * scale;
		z = s1 * scale;
		w = s2 * scale;

		x = 1 - (y*y) - (z*z) - (w*w);
		if (x > FLT_EPSILON):
			x = sqrt(x);
	return x,y,z,w		


	
def quatDecompress2(s0,s1,s2):

	AxisFlg = ((s1 & 1) << 1) | (s2 & 1)

	s0 = 1.41421*(s0-32767)/0x7FFF
	s1 = 1.41421*(s1-0x3FFF)/0x7FFF
	s2 = 1.41421*(s2-0x3FFF)/0x7FFF
	s3=1-(s0*s0+s1*s1+s2*s2)
	if s3>0:
		s3 = sqrt(s3)
	#print s0,s1,s2,s3,AxisFlg

	if AxisFlg==3:return s2, s1, s0, s3
	elif AxisFlg==2:return s2, s1 ,s3 ,s0
	elif AxisFlg==1:return s2, s3, s1 ,s0
	elif AxisFlg==0:return s3, s2, s1 ,s0
	
		
		