
from myFunction import *
import Blender
from Blender.Mathutils import *
import bpy

#Strife Online nowy euler

class Bone:
	def __init__(self):
		self.ID=None
		self.name=None
		self.parentID=None
		self.parentName=None
		self.quat=None
		self.pos=None
		self.matrix=None
		self.posMatrix=None
		self.rotMatrix=None
		self.scaleMatrix=None
		self.children=[]
		self.edit=None
	


class Skeleton:
	def __init__(self):
		self.name=None
		self.boneList=[]
		self.armature=None  
		self.object=None
		self.boneNameList=[] 
		self.ARMATURESPACE=False
		self.BONESPACE=True
		self.INVERTSPACE=False
		self.DEL=True
		self.NICE=False
		self.IK=False
		self.BINDMESH=False
		self.WARNING=False
		self.debug=None
		self.debugFile=None
		self.SORT=False
		self.matrix=None
		self.parentTestFlag=False
		self.nameTestFlag=False
		self.parentProblemList=[]
		self.nameProblemList=[]
		self.param=0.01
		self.JOIN=False
		
	def testParent(self):
		#self.parentTestFlag=False
		for bone in self.boneList:
			bone.parentList=[]
			if bone.name is not None:
			#print bone.name,bone.parentName
				for parent in self.boneList:
					if parent.name!=bone.name:
						if bone.parentName==parent.name:
							bone.parentList.append(parent)
		for bone in self.boneList:
			if len(bone.parentList)>1:
				self.parentTestFlag=True
				self.parentProblemList.append(bone)
				
	def testLongName(self):
		for bone in self.boneList:
			if bone.name is not None:
				if len(bone.name)>25:
					self.nameTestFlag=True
					self.nameProblemList.append(bone)
					#print 'Problem:name too long for bone',bone.name
				
		
	def boneChildren(self,parentBlenderBone,parentBone):
		for child in parentBlenderBone.children:
			for bone in self.boneList:
				if bone.name==child.name:
					blenderBone=self.armature.bones[bone.name]
					bone.matrix*=parentBone.matrix
					self.boneChildren(blenderBone,bone)
		
	def createChildList(self):
		for boneID in range(len(self.boneList)):
			bone=self.boneList[boneID]
			name=bone.name
			blenderBone=self.armature.bones[name]
			if blenderBone.parent is None:
				self.boneChildren(blenderBone,bone)
		
	def draw(self):
		if self.ARMATURESPACE==True:
			self.BONESPACE=False
			self.INVERTSPACE=False
		if self.INVERTSPACE==True:
			self.BONESPACE=False
			self.ARMATURESPACE=False
		if self.BONESPACE==True:
			self.ARMATURESPACE=False
			self.INVERTSPACE=False
		objectID=SceneIDList().szkieletID
		if not self.name:self.name='szkielet-'+str(objectID)
		if self.WARNING==True:
			print 'INPUT:'
			print 'class<Skeleton>.name:',self.name
			print 'class<Skeleton>.boneList:',len(self.boneList)
			print 'class<Skeleton>.ARMATURESPACE:',self.ARMATURESPACE
			print 'class<Skeleton>.BONESPACE:',self.BONESPACE
			
		if self.debug is not None:
			self.debugFile=open(self.debug+'.skeleton','w')
			
		#self.create_bones()
		self.testLongName()
		self.testParent()
		if self.parentTestFlag==False and self.nameTestFlag==False:
			self.check()
			if len(self.boneList)>0:
				self.create_bones()
				self.create_bone_connection()
				if self.SORT==True:
					self.createChildList()
				self.create_bone_position()			
			if self.BINDMESH is True:
				scene = bpy.data.scenes.active
				for object in scene.objects:
					if object.getType()=='Mesh':
						self.object.makeParentDeform([object],1,0)
			if self.IK==True:
				self.armature.drawType=Blender.Armature.OCTAHEDRON
				for key in self.armature.bones.keys():
					bone=self.armature.bones[key]
					#print bone
					children=bone.children
					if len(children)==1:
						self.armature.makeEditable()
						ebone=self.armature.bones[bone.name]
						#self.armature.bones[children[0].name].options=Blender.Armature.CONNECTED
						if ebone.tail!=children[0].head['ARMATURESPACE']:
							ebone.tail=children[0].head['ARMATURESPACE']
						self.armature.update()	
				for key in self.armature.bones.keys():
					bone=self.armature.bones[key]
					#print bone
					children=bone.children
					if len(children)==1:
						self.armature.makeEditable()
						self.armature.bones[children[0].name].options=Blender.Armature.CONNECTED
						self.armature.update()
				if self.IK==True:
					self.armature.autoIK=True
			return 1		
		else:
			print
			print '=======PROBLEMY==========='
			if self.parentTestFlag is True:
				print 'WARNING:znaleziono kosci z wiecej niz jednym rodzicem'
				for bone in self.parentProblemList:
					print bone.name,len(bone.parentList),'rodzic'
					for parent in bone.parentList:
						print ' '*4,parent.name
			if self.nameTestFlag is True:
				print 'WARNING:znaleziono kosci o za dlugiej nazwie'
				for bone in self.nameProblemList:
					print bone.name,len(bone.name),'liter'
			print		
			return 0
					
		if self.debug is not None:
			self.debugFile.close()
			


	def create_bones(self): 
		self.armature.makeEditable()
		boneList=[]
		for bone in self.armature.bones.values():
			if bone.name not in boneList:
				boneList.append(bone.name)
		for boneID in range(len(self.boneList)):
			name=self.boneList[boneID].name
			if self.debug is not None:
				self.debugFile.write(name+'\n')
			if name is None:
				name=str(boneID)
				self.boneList[boneID].name=name
			self.boneNameList.append(name)
			if name not in boneList:
				eb = Blender.Armature.Editbone() 
				self.armature.bones[name] = eb
		self.armature.update()
		
	def create_bone_connection(self):
		self.armature.makeEditable()
		for boneID in range(len(self.boneList)):
			name=self.boneList[boneID].name
			if name is None:
				name=str(boneID)
			bone=self.armature.bones[name]
			parentID=None
			parentName=None
			if self.boneList[boneID].parentID is not None:
				parentID=self.boneList[boneID].parentID
				if parentID!=-1:
					parentName=self.boneList[parentID].name
			if self.boneList[boneID].parentName is not None:
				parentName=self.boneList[boneID].parentName
			if parentName is not None:  
				parent=self.armature.bones[parentName]
				if parentID is not None:
					if parentID!=-1:
						bone.parent=parent
				else:
					bone.parent=parent
					
			else:
				if self.WARNING==True:
					print 'WARNING: no parent for bone',name
		self.armature.update()
		
		
		
	def create_bone_position(self):
		self.armature.makeEditable()
		for m in range(len(self.boneList)):
			name=self.boneList[m].name
			rotMatrix=self.boneList[m].rotMatrix
			posMatrix=self.boneList[m].posMatrix
			scaleMatrix=self.boneList[m].scaleMatrix
			matrix=self.boneList[m].matrix
			bone = self.armature.bones[name]
			if matrix is not None:
				if self.ARMATURESPACE==True:
					bone.matrix=matrix					
					if self.NICE==True:
						bvec = bone.tail- bone.head
						bvec.normalize()
						bone.tail = bone.head + self.param* bvec
				elif self.BONESPACE==True:
					rotMatrix=matrix.rotationPart()
					posMatrix=matrix.translationPart()
					scalePart=matrix.scalePart()
					if bone.parent:
						bone.head =   posMatrix * bone.parent.matrix+bone.parent.head
						tempM = rotMatrix * bone.parent.matrix 
						bone.matrix = tempM
					else:
						bone.head = posMatrix
						bone.matrix = rotMatrix
					if self.NICE==True:
						bvec = bone.tail- bone.head
						bvec.normalize()
						bone.tail = bone.head + self.param * bvec  
				elif self.INVERTSPACE==True:
					rotMatrix=matrix.rotationPart()
					posMatrix=matrix.translationPart()
					posMatrix=posMatrix*rotMatrix.invert()
					posMatrix.negate()
					if bone.parent:
						bone.head =   posMatrix
						tempM = bone.parent.matrix*rotMatrix
						bone.matrix = tempM
					else:
						bone.head = posMatrix
						bone.matrix = rotMatrix
					if self.NICE==True:
						bvec = bone.tail- bone.head
						bvec.normalize()
						bone.tail = bone.head + self.param * bvec  	
						
				else:
					if self.WARNING==True:
						print 'ARMATUREPACE or BONESPACE ?'	
			elif rotMatrix is not None and posMatrix is not None:
				if self.ARMATURESPACE==True:
					rotMatrix=roundMatrix(rotMatrix,4)
					posMatrix=roundMatrix(posMatrix,4)
					bone.matrix=rotMatrix*posMatrix
					if self.NICE==True:
						bvec = bone.tail- bone.head
						bvec.normalize()
						bone.tail = bone.head + self.param * bvec
				elif self.BONESPACE==True:
					rotMatrix=roundMatrix(rotMatrix,4).rotationPart()
					posMatrix=roundMatrix(posMatrix,4).translationPart()
					if bone.parent:
						bone.head =   posMatrix * bone.parent.matrix+bone.parent.head
						tempM = rotMatrix * bone.parent.matrix 
						bone.matrix = tempM
					else:
						bone.head = posMatrix
						bone.matrix = rotMatrix
					if self.NICE==True:
						bvec = bone.tail- bone.head
						bvec.normalize()
						bone.tail = bone.head + self.param * bvec 
				else:
					if self.WARNING==True:
						print 'ARMATUREPACE or BONESPACE ?'	
			else:
				if self.WARNING==True:
					print 'WARNINIG: rotMatrix or posMatrix or matrix is None'
							
		self.armature.update()
		Blender.Window.RedrawAll()
		
		
		
	def check(self):
		scn = Blender.Scene.GetCurrent()
		scene = bpy.data.scenes.active
		for object in scene.objects:
			if object.getType()=='Armature':
				if object.name == self.name:
					scene.objects.unlink(object)
		for object in bpy.data.objects:
			if object.name == self.name:
				self.object = Blender.Object.Get(self.name)
				self.armature = self.object.getData()
				if self.DEL==True:  
					self.armature.makeEditable()
					for bone in self.armature.bones.values():
						del self.armature.bones[bone.name]
					self.armature.update()
		if self.object==None: 
			self.object = Blender.Object.New('Armature',self.name)
		if self.armature==None: 
			self.armature = Blender.Armature.New(self.name)
			self.object.link(self.armature)
		scn.link(self.object)
		self.armature.drawType = Blender.Armature.STICK
		self.object.drawMode = Blender.Object.DrawModes.XRAY
		self.matrix=self.object.mat
	
		
	def check1(self):
		scn = Blender.Scene.GetCurrent()
		scene = bpy.data.scenes.active
		self.object = Blender.Object.New('Armature',self.name)
		self.armature = Blender.Armature.New(self.name)
		self.object.link(self.armature)
		scn.link(self.object)
		self.armature.drawType = Blender.Armature.STICK
		self.object.drawMode = Blender.Object.DrawModes.XRAY
	
	


class Node():
	def __init__(self):
		self.name=None
		self.offset=None
		self.children=[]
		self.dataL=''
		self.dataU=''
	def values(self,data):
		lines=data.split('\x0a')
		list={}
		for line in lines:
			lineStrip=line.strip().replace(',',' ')
			
			if len(lineStrip)>0:
				if ':' in lineStrip:
					lineSplit=line.split(':')
					if '"' in lineSplit[0]:
						key=lineSplit[0].split('"')[1]
						print 'key',key
					if '"' in lineSplit[1]:
						data=lineSplit[1].split('"')[1]
						print 'data',data
						
						
			