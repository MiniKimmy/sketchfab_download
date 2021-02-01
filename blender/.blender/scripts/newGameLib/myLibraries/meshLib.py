import bpy
import Blender
from Blender.Mathutils import *
from myFunction import *
from commandLib import *
import random
import os
#from bump_to_normal import *

#print 'meshLib'
   
def GetAlphaFromImage(path):

	sys=Sys(path)
	image = Blender.Image.Load(path)
	imagedepth=image.getDepth() 
	imagesize = image.getSize()
	imagenewname=sys.dir+os.sep+sys.base+'-alfa.tga'
	
	
	img=Sys(imagenewname)
	ImgPath=img.dir+os.sep+img.base+'.jpg'
	
	if os.path.exists(ImgPath)==False:
		#print imagenewname
		imagenew = Blender.Image.New(imagenewname,imagesize[0],imagesize[1],imagedepth) 
		for x in range(0,imagesize[0]):
			for y in range(0,imagesize[1]):
				pix=image.getPixelI(x, y)[3]	
				imagenew.setPixelI(x,y,[255-pix,255-pix,255-pix,0])
		imagenew.save()
	
	
			
		cmd=Cmd()
		cmd.input=imagenewname
		cmd.JPG=True
		cmd.run()
	return ImgPath  
	
def GetBlackFromImage(path):

	sys=Sys(path)
	image = Blender.Image.Load(path)
	imagedepth=image.getDepth() 
	imagesize = image.getSize()
	imagenewname=sys.dir+os.sep+sys.base+'-alfa.tga'
	
	
	img=Sys(imagenewname)
	ImgPath=img.dir+os.sep+img.base+'.jpg'
	
	if os.path.exists(ImgPath)==False:
		#print imagenewname
		imagenew = Blender.Image.New(imagenewname,imagesize[0],imagesize[1],imagedepth) 
		for x in range(0,imagesize[0]):
				for y in range(0,imagesize[1]):
					pix=image.getPixelI(x, y)
					if 125<pix[0]<135 and 121<pix[1]<131 and 57<pix[2]<67:
					#if pix[0]==130 and pix[1]==126 and pix[2]==62:
						#print pix
						imagenew.setPixelI(x,y,[0,0,0,0])
					else:
						#imagenew.setPixelI(x,y,[255-pix[0],255-pix[1],255-pix[2],0])
						imagenew.setPixelI(x,y,[255,255,255,0])
		imagenew.save()
		
		
				
		cmd=Cmd()
		cmd.input=imagenewname
		cmd.JPG=True
		cmd.run()
	return ImgPath 
	
def setBox(box,meshList):
	E=[[],[],[]]
	for mesh in meshList:
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			E[0].append(x)
			E[1].append(y)
			E[2].append(z)	
	skX=(box[3]-box[0])/(max(E[0])-min(E[0]))
	skY=(box[4]-box[1])/(max(E[1])-min(E[1]))
	skZ=(box[5]-box[2])/(max(E[2])-min(E[2]))
	sk=min(skX,skY,skZ)
	trX1=(box[3]+box[0])/2#-(max(E[0])+min(E[0]))/2
	trY1=(box[4]+box[1])/2#-(max(E[1])+min(E[1]))/2
	trZ1=(box[5]+box[2])/2#-(max(E[2])+min(E[2]))/2
	
	trX=-(max(E[0])+min(E[0]))/2
	trY=-(max(E[1])+min(E[1]))/2
	trZ=-(max(E[2])+min(E[2]))/2
	#print trX,trY,trZ
	#print skX,skY,skZ
	
	for mesh in meshList:
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[x+trX,y+trY,z+trZ]
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[x*skX,y*skY,z*skZ]
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[x+trX1,y+trY1,z+trZ1]
		#mesh.draw()	 
		
def setBox1(box,meshList):
	E=[[],[],[]]
	for mesh in meshList:
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			E[0].append(x)
			E[1].append(y)
			E[2].append(z)	
	skX=(box[3]-box[0])/(max(E[0])-min(E[0]))
	skY=(box[4]-box[1])/(max(E[1])-min(E[1]))
	skZ=(box[5]-box[2])/(max(E[2])-min(E[2]))
	sk=min(skX,skY,skZ)
	trX=(box[3]+box[0])/2
	trY=(box[4]+box[1])/2
	trZ=(box[5]+box[2])/2
	
	
	for mesh in meshList:
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[trX+x*skX,trY+y*skY,trZ+z*skZ]
		#mesh.draw()	



def bindPose(bindSkeleton,poseSkeleton,meshObject):
		#print 'BINDPOSE'
		mesh=meshObject.getData(mesh=1)
		poseBones=poseSkeleton.getData().bones
		bindBones=bindSkeleton.getData().bones			
		for vert in mesh.verts:
			index=vert.index
			skinList=mesh.getVertexInfluences(index)
			vco=vert.co.copy()*meshObject.matrixWorld
			vector=Vector()
			sum=0
			for skin in skinList:
				#try:
					bone=skin[0]							
					weight=skin[1]					
					matA=bindBones[bone].matrix['ARMATURESPACE']*bindSkeleton.matrixWorld
					matB=poseBones[bone].matrix['ARMATURESPACE']*poseSkeleton.matrixWorld
					vector+=vco*matA.invert()*matB*weight
					sum+=weight
				#except:pass	
			#print sum,	
			vert.co=vector
		mesh.update()
		Blender.Window.RedrawAll()
			
			
#ID=3
#bindSkeleton=Blender.Object.Get('armature-'+str(ID))
#poseSkeleton=Blender.Object.Get('bindPose-mesh-'+str(ID))
#meshObject=Blender.Object.Get('mesh-'+str(ID))

#bindPose(bindSkeleton,poseSkeleton,meshObject)	


class Model:
	def __init__(self,input):
		self.meshList=[]
		self.filename=input
		self.dirname=None
		self.basename=None
		#if self.filename is not None
		
		
	def getMat(self):#	
		if self.filename is not None and self.meshList>0:
			self.basename=os.path.basename(self.filename)
			self.dirname=os.path.dirname(self.filename)
			#matPath=self.dirname+os.sep+'mat.txt'
			matPath=self.filename+'.mat'
			if os.path.exists(matPath)==True:
				matfile=open(matPath,'r')
				lines=matfile.readlines()
				for i,mesh in enumerate(self.meshList):
					for j,mat in enumerate(mesh.matList):
						for line in lines:
							values=line.strip().split(':')
							if values[0]=="-1":i=-1#pierwszy raz 
							if len(values)==3:
								if values[0]==str(i).zfill(3) and values[1]=='d':mat.diffuse=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='n':mat.normal=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='s':mat.specular=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='a':mat.alpha=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='o':mat.ao=self.dirname+os.sep+values[2].split('"')[1]
								
								if values[0]==str(i).zfill(3) and values[1]=='d1':mat.diffuse1=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='d2':mat.diffuse2=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='n1':mat.normal1=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='n2':mat.normal2=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='e':mat.emit=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='b':mat.bump=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='t':mat.trans=self.dirname+os.sep+values[2].split('"')[1]
							if len(values)==4:
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='d':mat.diffuse=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='n':mat.normal=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='s':mat.specular=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='a':mat.alpha=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='o':mat.ao=self.dirname+os.sep+values[2].split('"')[1]
								
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='d1':mat.diffuse1=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='d2':mat.diffuse2=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='n1':mat.normal1=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='n2':mat.normal2=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='e':mat.emit=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='b':mat.bump=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='t':mat.trans=self.dirname+os.sep+values[2].split('"')[1]
				for i,mesh in enumerate(self.meshList):
					for j,mat in enumerate(mesh.matList):
						for line in lines:
							values=line.strip().split(':')
							#if values[0]=="-1":i=-1
							if len(values)==3:
								if values[0]==str(i).zfill(3) and values[1]=='d':mat.diffuse=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='n':mat.normal=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='s':mat.specular=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='a':mat.alpha=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='o':mat.ao=self.dirname+os.sep+values[2].split('"')[1]
								
								if values[0]==str(i).zfill(3) and values[1]=='d1':mat.diffuse1=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='d2':mat.diffuse2=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='n1':mat.normal1=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='n2':mat.normal2=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='e':mat.emit=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='b':mat.bump=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[1]=='t':mat.trans=self.dirname+os.sep+values[2].split('"')[1]
							if len(values)==4:
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='d':mat.diffuse=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='n':mat.normal=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='s':mat.specular=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='a':mat.alpha=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='o':mat.ao=self.dirname+os.sep+values[2].split('"')[1]
								
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='d1':mat.diffuse1=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='d2':mat.diffuse2=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='n1':mat.normal1=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='n2':mat.normal2=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='e':mat.emit=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='b':mat.bump=self.dirname+os.sep+values[2].split('"')[1]
								if values[0]==str(i).zfill(3) and values[3]==str(j) and values[1]=='t':mat.trans=self.dirname+os.sep+values[2].split('"')[1]
						#print i,j,mat.diffuse	"""		
				matfile.close()
		
	def setMat(self):
		#print 'setMat'
		if self.filename is not None and self.meshList>0:
			self.basename=os.path.basename(self.filename)
			self.dirname=os.path.dirname(self.filename)
			#matPath=self.dirname+os.sep+'mat.txt'
			matPath=self.filename+'.mat'
			#for file in os.listdir(self.dirname):
			#	if file.lower()=='mat.txt':
			matLines=[]
			if os.path.exists(matPath)==True:
					file=open(matPath,'r')
					lines=file.readlines()
					for line in lines:
						if ':' in line:
							matLines.append(line)
					file.close()
					
			#if 'mat.txt' not in os.listdir(os.path.dirname(filename)):
			matFile=open(matPath,'w')
			for file in os.listdir(self.dirname):
				if file.split('.')[-1].lower() in ['dds','png','jpg','jpeg','tga','bmp']:
					matFile.write('"'+file+'"'+'\n')
					
			for i,mesh in enumerate(self.meshList):
				for j,mat in enumerate(mesh.matList):
					#print mat.name
					split=mat.name.split('-')
					if mat.diffuse is not None:matFile.write(str(split[0])+':d:"'+os.path.basename(mat.diffuse)+'":'+str(split[1])+'\n')
					if mat.normal is not None:matFile.write(str(split[0])+':n:"'+os.path.basename(mat.normal)+'":'+str(split[1])+'\n')
					if mat.specular is not None:matFile.write(str(split[0])+':s:"'+os.path.basename(mat.specular)+'":'+str(split[1])+'\n')
					if mat.ao is not None:matFile.write(str(split[0])+':o:"'+os.path.basename(mat.ao)+'":'+str(split[1])+'\n')
					if mat.alpha is not None:matFile.write(str(split[0])+':a:"'+os.path.basename(mat.alpha)+'":'+str(split[1])+'\n')
					
					if mat.diffuse1 is not None:matFile.write(str(split[0])+':d1:"'+os.path.basename(mat.diffuse1)+'":'+str(split[1])+'\n')
					if mat.diffuse2 is not None:matFile.write(str(split[0])+':d2:"'+os.path.basename(mat.diffuse2)+'":'+str(split[1])+'\n')
					if mat.normal1 is not None:matFile.write(str(split[0])+':n1:"'+os.path.basename(mat.normal1)+'":'+str(split[1])+'\n')
					if mat.normal2 is not None:matFile.write(str(split[0])+':n2:"'+os.path.basename(mat.normal2)+'":'+str(split[1])+'\n')
					if mat.emit is not None:matFile.write(str(split[0])+':e:"'+os.path.basename(mat.emit)+'":'+str(split[1])+'\n')
					if mat.bump is not None:matFile.write(str(split[0])+':b:"'+os.path.basename(mat.bump)+'":'+str(split[1])+'\n')
					if mat.trans is not None:matFile.write(str(split[0])+':t:"'+os.path.basename(mat.trans)+'":'+str(split[1])+'\n')
					
					
			matFile.close()
	def draw(self):
		for i,mesh in enumerate(self.meshList):
			#print 'mesh:',i,'vert:',len(mesh.vertPosList),'indice:',len(mesh.indiceList),
			#if len(mesh.indiceList)>0:
			#	print 'min:',min(mesh.indiceList),'max:',max(mesh.indiceList),
			#print 'face:',len(mesh.faceList)	
			mesh.draw()
						
		
		
			
class Mesh():
	
	def __init__(self):
		self.vertPosList=[]
		self.vertNormList=[]
		
		self.indiceList=[]
		self.faceList=[]
		self.triangleList=[]
		
		self.matList=[]
		self.matIDList=[]
		self.vertUVList=[]
		self.faceUVList=[]
		
		self.skinList=[]
		self.skinWeightList=[]
		self.skinIndiceList=[]
		self.skinGroupList=[]
		self.skinIDList=[]
		self.bindPoseMatrixList=[]
		self.boneNameList=[]
		
		self.name=None
		self.mesh=None
		self.object=None
		self.TRIANGLE=False
		self.QUAD=False
		self.TRISTRIP=False
		self.BINDSKELETON=None
		self.BINDPOSESKELETON=None
		self.matrix=None
		self.SPLIT=False
		self.WARNING=False
		self.DRAW=False
		self.BINDPOSE=False
		self.UVFLIP=False
		self.sceneIDList=None
		
		self.vertModList=[]
		self.mod=False
		self.filename=None
		
		
	def addMat(self,mat,mesh,matID):
		#if mat.name is None:
		#	mat.name=self.name+'-mat-'+str(matID)
		#mat.name=mesh.name
		mat.name=mesh.name.split('-')[0]+'-'+str(matID)+'-'+str(self.sceneIDList.objectID)
		blendMat=Blender.Material.New(mat.name)
		blendMat.diffuseShader=Blender.Material.Shaders.DIFFUSE_ORENNAYAR
		blendMat.specShader=Blender.Material.Shaders.SPEC_WARDISO
		blendMat.setRms(0.04)
		blendMat.shadeMode=Blender.Material.ShadeModes.CUBIC
		if mat.rgbCol is None:
			blendMat.rgbCol=mat.rgba[:3]
			blendMat.alpha = mat.rgba[3]
		else:
			blendMat.rgbCol=mat.rgbCol[:3]
			#blendMat.alpha = mat.rgba[3]
		if mat.rgbSpec is not None:
			blendMat.specCol=mat.rgbSpec[:3]
			
		if mat.ZTRANS==True:
			blendMat.mode |= Blender.Material.Modes.ZTRANSP
			blendMat.mode |= Blender.Material.Modes.TRANSPSHADOW 
			blendMat.alpha = 0.0 
		if mat.diffuse is not None:diffuse(blendMat,mat)
		if mat.reflection is not None:reflection(blendMat,mat)
		if mat.diffuse1 is not None:diffuse1(blendMat,mat)
		if mat.diffuse2 is not None:diffuse2(blendMat,mat)
		if mat.specular is not None:specular(blendMat,mat)
		if mat.normal is not None:normal(blendMat,mat)
		if mat.bump is not None:bump(blendMat,mat)
		if mat.normal1 is not None:normal1(blendMat,mat)
		if mat.normal2 is not None:normal2(blendMat,mat)
		if mat.ao is not None:ao(blendMat,mat)
		if mat.alpha is not None:alpha(blendMat,mat)
		if mat.emit is not None:emit(blendMat,mat)
		if mat.trans is not None:trans(blendMat,mat)
		mesh.materials+=[blendMat]	
		
		
	def addvertexUV(self,blenderMesh,mesh): 
		blenderMesh.vertexUV = 1
		for m in range(len(blenderMesh.verts)):
			if self.UVFLIP==False:blenderMesh.verts[m].uvco = Vector(mesh.vertUVList[m][0],1-mesh.vertUVList[m][1])	
			else:blenderMesh.verts[m].uvco = Vector(mesh.vertUVList[m])
		
		
	def addfaceUV(self,blenderMesh,mesh):
		if self.WARNING==True:
			print 'WARNING: blenderMesh.faces:',len(blenderMesh.faces)
		if len(blenderMesh.faces)>0:
			blenderMesh.faceUV = 1
			if len(mesh.vertUVList)>0:
				for ID in range(len(blenderMesh.faces)):			
					face=blenderMesh.faces[ID]
					face.uv = [v.uvco for v in face.verts]
					face.smooth = 1
					if len(mesh.matIDList)>0:
						face.mat=mesh.matIDList[ID] 
			if len(mesh.matIDList)>0:
				for ID in range(len(blenderMesh.faces)):	
					face=blenderMesh.faces[ID]
					face.smooth = 1 
					#print ID,len(mesh.matIDList)
					face.mat=mesh.matIDList[ID]
			if len(mesh.faceUVList)>0:
				for ID in range(len(blenderMesh.faces)): 
					face=blenderMesh.faces[ID]
					if mesh.faceUVList[ID] is not None:
						face.uv=mesh.faceUVList[ID]
			if len(self.vertNormList)==0:			
				blenderMesh.calcNormals()	
			blenderMesh.update() 
	
	def addSkinIDList(self):
		if len(self.skinIDList)==0:
			for m in range(len(self.vertPosList)):
				self.skinIDList.append([])
				for n in range(len(self.skinList)):
					self.skinIDList[m].append(0)
			for skinID in range(len(self.skinList)):
				skin=self.skinList[skinID]
				if skin.IDStart==None:
					skin.IDStart=0
				if skin.IDCount==None:
					skin.IDCount=len(self.vertPosList)
				for vertID in range(skin.IDStart,skin.IDStart+skin.IDCount):
					self.skinIDList[vertID][skinID]=1
			
			
	def addSkinWithIndiceList(self,blendMesh,mesh):
		#print 'addskin'
		for vertID in range(len(mesh.skinIDList)):
			indices=mesh.skinIndiceList[vertID]
			weights=mesh.skinWeightList[vertID]
			#print mesh.skinIDList[vertID]
			for skinID,ID in enumerate(mesh.skinIDList[vertID]):
				if ID==1:
					if len(weights)<len(indices):count=len(weights)
					else:count=len(indices)
					for n in range(count):
						w  = weights[n]
						if type(w)==int:w=w/255.0
						if w!=0.0:
							grID = indices[n]
							if len(self.boneNameList)==0:
								if len(self.skinList[skinID].boneMap)>0:grName = str(self.skinList[skinID].boneMap[grID])
								else:grName = str(grID)
							else:	
								if len(self.skinList[skinID].boneMap)>0:
									grNameID = self.skinList[skinID].boneMap[grID]
									grName=self.boneNameList[grNameID]
								else:	
									grName=self.boneNameList[grID]
							if grName not in blendMesh.getVertGroupNames():
								blendMesh.addVertGroup(grName)
							add = Blender.Mesh.AssignModes.ADD
							blendMesh.assignVertsToGroup(grName,[vertID],w,add)
		blendMesh.update()
			
		
	def addSkinWithGroupList(self,blendMesh,mesh):
		#print 'addskin'
		for vertID in range(len(mesh.skinIDList)):
			groups=mesh.skinGroupList[vertID]
			weights=mesh.skinWeightList[vertID]
			#print mesh.skinIDList[vertID]
			for skinID,ID in enumerate(mesh.skinIDList[vertID]):
				if ID==1:
					if len(weights)<len(groups):count=len(weights)
					else:count=len(groups)
					for n in range(count):
						w  = weights[n]
						if type(w)==int:w=w/255.0
						if w!=0.0:
							grName=groups[n]
							if grName not in blendMesh.getVertGroupNames():
								blendMesh.addVertGroup(grName)
							add = Blender.Mesh.AssignModes.ADD
							blendMesh.assignVertsToGroup(grName,[vertID],w,add)
		blendMesh.update()
			
		
	def addSkin(self,blendMesh,mesh):
		#print 'addskin'
		for vertID in range(len(mesh.skinIDList)):
			indices=mesh.skinIndiceList[vertID]
			weights=mesh.skinWeightList[vertID]
			#print mesh.skinIDList[vertID]
			for skinID,ID in enumerate(mesh.skinIDList[vertID]):
				if ID==1:
					if len(weights)<len(indices):count=len(weights)
					else:count=len(indices)
					#print indices,weights
					for n in range(count):
						w  = weights[n]
						if type(w)==int:w=w/255.0
						if w!=0.0:
							grID = indices[n]
							if len(self.boneNameList)==0:
								if len(self.skinList[skinID].boneMap)>0:grName = str(self.skinList[skinID].boneMap[grID])
								else:grName = str(grID)
							else:	
								if len(self.skinList[skinID].boneMap)>0:
									grNameID = self.skinList[skinID].boneMap[grID]
									grName=self.boneNameList[grNameID]
								else:	
									grName=self.boneNameList[grID]
							if grName not in blendMesh.getVertGroupNames():
								blendMesh.addVertGroup(grName)
							add = Blender.Mesh.AssignModes.ADD
							blendMesh.assignVertsToGroup(grName,[vertID],w,add)
		blendMesh.update()
			
		
		
	def addFaces(self): 
		if len(self.matList)==0:
			if len(self.faceList)!=0:
				self.triangleList=self.faceList
			if len(self.indiceList)!=0:
				if self.TRIANGLE==True:
					self.indicesToTriangles(self.indiceList,0)
				elif self.QUAD==True:
					self.indicesToQuads(self.indiceList,0)
				elif self.TRISTRIP==True:
					self.indicesToTriangleStrips(self.indiceList,0)
				else:
					if self.WARNING==True:
						print 'WARNING: class<Mesh>.TRIANGLE:',self.TRIANGLE 
						print 'WARNING: class<Mesh>.TRISTRIP:',self.TRISTRIP
				
					
		else:
			if len(self.faceList)>0:
				if len(self.matIDList)==0:
					for matID in range(len(self.matList)):
						mat=self.matList[matID] 
						if mat.IDStart is not None and mat.IDCount is not None:
							for faceID in range(mat.IDCount):
								self.triangleList.append(self.faceList[mat.IDStart+faceID])
								self.matIDList.append(matID)
						else:
							if mat.IDStart==None:
								mat.IDStart=0
							if mat.IDCount==None:
								mat.IDCount=len(self.faceList)
							for faceID in range(mat.IDCount):
								self.triangleList.append(self.faceList[mat.IDStart+faceID])
								self.matIDList.append(matID)
					#self.triangleList=self.faceList
							
								
				else:			
					self.triangleList=self.faceList
					#for ID in range(len(self.matIDList)):
					#	mat=self.matList[matID] 
						#if self.matIDList[ID]==matID:
					#	self.triangleList.append(self.faceList[ID])
						
			if len(self.indiceList)>0:
				if len(self.matIDList)==0:
					for matID in range(len(self.matList)):
						mat=self.matList[matID] 
						if mat.IDStart==None:
							mat.IDStart=0
						if mat.IDCount==None:
							mat.IDCount=len(self.indiceList)
						indiceList=self.indiceList[mat.IDStart:mat.IDStart+mat.IDCount]					
						if mat.TRIANGLE==True:
							self.indicesToTriangles(indiceList,matID)
						elif mat.QUAD==True:
							self.indicesToQuads(indiceList,matID)
						elif mat.TRISTRIP==True:
							self.indicesToTriangleStrips(indiceList,matID)
				"""else:			
						
						if mat.TRIANGLE==True:
							self.indicesToTriangles2(indiceList)
						elif mat.QUAD==True:
							self.indicesToQuads2(indiceList)
						elif mat.TRISTRIP==True:
							self.indicesToTriangleStrips2(indiceList)"""
					
					
			
	def setBoneMatrix(self,skeletonName,boneName):
		scene = bpy.data.scenes.active
		for object in scene.objects:
			if object.name==skeletonName:
				bones=object.getData().bones
				if boneName in bones.keys():
					matrix=bones[boneName].matrix['ARMATURESPACE']
					#self.object.setMatrix(matrix*self.object.matrixWorld)
					#print boneName,matrix
					self.object.setMatrix(matrix)

	def buildMesh(self,mesh,mat,meshID):
		blendMesh = bpy.data.meshes.new(mesh.name)
		blendMesh.verts.extend(mesh.vertPosList)			
		blendMesh.faces.extend(mesh.triangleList,ignoreDups=True)
		self.addMat(mat,blendMesh,meshID)	
		if len(mesh.triangleList)>0:	
			if len(mesh.vertUVList)>0:
				self.addvertexUV(blendMesh,mesh)
				self.addfaceUV(blendMesh,mesh)
			if len(mesh.faceUVList)>0:
				self.addfaceUV(blendMesh,mesh)
		if len(mesh.vertNormList)>0:
			for i,vert in enumerate(blendMesh.verts):
				vert.no=Vector(self.vertNormList[i])
			
		scene = bpy.data.scenes.active
		meshobject = scene.objects.new(blendMesh,mesh.name)
		
		
		try:self.addSkinWithIndiceList(blendMesh,mesh)
		except:print 'WARNING:self.addSkinWithIndiceList:',mesh.name
		
		
		Blender.Window.RedrawAll()
		if self.BINDSKELETON is not None:
			for object in scene.objects:
				if object.name==self.BINDSKELETON:
					#meshobject.mat*=object.mat
					object.makeParentDeform([meshobject],1,0)
		if mat.matrix is not None:
			#blendMesh.transform(self.matrix)
			meshobject.setMatrix(mat.matrix*meshobject.matrixWorld)
		if mat.BINDSKELETON is not None:
			for object in scene.objects:
				if object.name==mat.BINDSKELETON:
					object.makeParentDeform([meshobject],1,0)
		Blender.Window.RedrawAll()	
		
	def addMesh(self):
		self.mesh = bpy.data.meshes.new(self.name)
		self.mesh.verts.extend(self.vertPosList)
		if len(self.vertNormList)>0:
			for i,vert in enumerate(self.mesh.verts):vert.no=Vector(self.vertNormList[i])			
		self.mesh.faces.extend(self.triangleList,ignoreDups=True)
		scene = bpy.data.scenes.active
		self.object = scene.objects.new(self.mesh,self.name)
		
		#if self.matrix is not None:
			#self.object.setMatrix(self.matrix*self.object.matrixWorld)
			#self.mesh.transform(self.matrix)		
			
			
			
		
	def draw(self): 
		#if self.name is None:
		#self.name=str(ParseID())+'-0-0'
		self.sceneIDList=SceneIDList()
		self.name=str(self.sceneIDList.meshID).zfill(3)+'-0-'+str(self.sceneIDList.objectID)
		self.addFaces() 
		if self.SPLIT==False:
			self.addMesh()
			if self.mod==True:
				modFile=open(self.name+'.txt','w')
				if self.filename is not None:
					modFile.write(self.filename+'\n')
				else:
					modFile.write('None'+'\n')
				for m in range(len(self.vertModList)):
					a,b,c=self.vertModList[m]
					modFile.write(str(a)+' '+str(b)+' '+str(c)+'\n')
				modFile.close()
			if len(self.triangleList)>0:	
				if len(self.vertUVList)>0:
					self.addvertexUV(self.mesh,self)
					#self.addfaceUV(self.mesh,self)
				#if len(self.faceUVList)>0:	
			self.addfaceUV(self.mesh,self)
			for matID in range(len(self.matList)):
				mat=self.matList[matID]
				self.addMat(mat,self.mesh,matID)
				
			if self.BINDSKELETON is not None:
				scene = bpy.data.scenes.active
				for object in scene.objects:
					if object.name==self.BINDSKELETON:
						skeletonMatrix=self.object.getMatrix()*object.mat
						#self.object.setMatrix(skeletonMatrix)
						object.makeParentDeform([self.object],1,0)
			if len(self.skinIndiceList)>0 and len(self.skinWeightList)>0:	
				if len(self.skinIndiceList)==len(self.skinWeightList)>0:
					try:				
						self.addSkinIDList()		
						self.addSkinWithIndiceList(self.mesh,self)
					#except:
					except:print 'WARNING:self.addSkinWithIndiceList:',self.mesh.name
			if len(self.skinGroupList)>0 and len(self.skinWeightList)>0:	
				if len(self.skinGroupList)==len(self.skinWeightList)>0:	
					#print 'addSkinWithGroupList'
					try:
						self.addSkinIDList()		
						self.addSkinWithGroupList(self.mesh,self)
					except:print 'WARNING:self.addSkinWithGroupList:',self.mesh.name
			Blender.Window.RedrawAll()		
			
			
		if self.SPLIT==True:
			#print 'Dzielenie siatek:',len(self.matList)
			#print 'self.name:',self.name
			meshList=[]
			for matID in range(len(self.matList)):
				mesh=Mesh()
				mesh.IDList={}
				mesh.IDCounter=0
				#if self.matList[matID].name is not None:
				#	mesh.name=self.matList[matID].name
				#else:	
				#	mesh.name=self.name+'-'+str(matID)
				mesh.name=self.name.split('-')[0]+'-'+str(matID)+'-'+str(self.sceneIDList.objectID)
				#print ' '*4,'siatka:',matID,mesh.name	
				meshList.append(mesh)			
					
			for faceID in range(len(self.matIDList)):
				matID=self.matIDList[faceID]
				mesh=meshList[matID]
				for vID in self.triangleList[faceID]:
					mesh.IDList[vID]=None
				
			for faceID in range(len(self.matIDList)):
				matID=self.matIDList[faceID]
				mesh=meshList[matID]
				for vID in self.triangleList[faceID]:
					if mesh.IDList[vID] is None:						
						mesh.IDList[vID]=mesh.IDCounter
						mesh.IDCounter+=1
				
				
			for faceID in range(len(self.matIDList)):
				matID=self.matIDList[faceID]
				mesh=meshList[matID]
				face=[]
				for vID in self.triangleList[faceID]:
					face.append(mesh.IDList[vID])
				#mesh.faceList.append(face)	
				mesh.triangleList.append(face)
				mesh.matIDList.append(0)
				if len(self.faceUVList)>0:
					mesh.faceUVList.append(self.faceUVList[faceID]) 
			for mesh in meshList:
				for m in range(len(mesh.IDList)):
					mesh.vertPosList.append(None)	
				if len(self.vertUVList)>0:
					for m in range(len(mesh.IDList)):
						mesh.vertUVList.append(None)	
				if len(self.skinList)>0:
					if len(self.skinIndiceList)>0 and len(self.skinWeightList)>0:
						for m in range(len(mesh.IDList)):	
							mesh.skinWeightList.append([])
							mesh.skinIndiceList.append([])
							mesh.skinIDList.append(None)
			if len(self.skinList)>0:
				if len(self.skinIndiceList)>0 and len(self.skinWeightList)>0:	
					if len(self.skinIDList)==0:				
						try:self.addSkinIDList()		
						except:print 'WARNING:self.addSkinIDList:',self.name
			for i,mesh in enumerate(meshList):
				#print mesh.IDList.keys()
				for vID in mesh.IDList.keys():
					mesh.vertPosList[mesh.IDList[vID]]=self.vertPosList[vID]
				if len(self.vertUVList)>0:
					for vID in mesh.IDList.keys():
						mesh.vertUVList[mesh.IDList[vID]]=self.vertUVList[vID]
				if len(self.skinList)>0:
					if len(self.skinIndiceList)>0 and len(self.skinWeightList)>0:	
						if len(self.skinIDList)>0:
							for vID in mesh.IDList.keys():	
								mesh.skinWeightList[mesh.IDList[vID]]=self.skinWeightList[vID]
								mesh.skinIndiceList[mesh.IDList[vID]]=self.skinIndiceList[vID]
								mesh.skinIDList[mesh.IDList[vID]]=self.skinIDList[vID]
						else:
							#mat=self.matList[i]]
							#if mat.IDStart is not None and mat.IDCount is not None:
							#	for 
							print 'self.skinIDList is missing'
					
			for meshID in range(len(meshList)):
				mesh=meshList[meshID]
				#print len(mesh.triangleList)
				mat=self.matList[meshID]
				self.buildMesh(mesh,mat,meshID)
				#mesh.matList.append(mat)
				#mesh.draw()
					
			Blender.Window.RedrawAll()	
			
				
				
	def indicesToQuads(self,indicesList,matID):
		for m in range(0, len(indicesList), 4):
			self.triangleList.append(indicesList[m:m+4] )
			self.matIDList.append(matID)
				
	def indicesToTriangles(self,indicesList,matID):
		for m in range(0, len(indicesList), 3):
			self.triangleList.append(indicesList[m:m+3] )
			self.matIDList.append(matID)
		

	def indicesToTriangleStrips(self,indicesList,matID):
		StartDirection = -1
		id=0
		f1 = indicesList[id]
		id+=1
		f2 = indicesList[id]
		FaceDirection = StartDirection
		while(True):
		#for m in range(len(indicesList)-2):
			id+=1
			f3 = indicesList[id]
			#print f3
			if (f3==0xFFFF):
				if id==len(indicesList)-1:break
				id+=1
				f1 = indicesList[id]
				id+=1
				f2 = indicesList[id]
				FaceDirection = StartDirection	 
			else:
				#f3 += 1
				FaceDirection *= -1
				if (f1!=f2) and (f2!=f3) and (f3!=f1):
					if FaceDirection > 0:						
						self.triangleList.append([(f1),(f2),(f3)])
						self.matIDList.append(matID)
					else:
						self.triangleList.append([(f1),(f3),(f2)])
						self.matIDList.append(matID)
					if self.DRAW==True: 
						f1,f2,f3	
				f1 = f2
				f2 = f3
			if id==len(indicesList)-1:break

				
	def indicesToQuads2(self,indicesList):
		for m in range(0, len(indicesList), 4):
			self.triangleList.append(indicesList[m:m+4] )
			#self.matIDList.append(matID)
				
	def indicesToTriangles2(self,indicesList):
		for m in range(0, len(indicesList), 3):
			self.triangleList.append(indicesList[m:m+3] )
			#self.matIDList.append(matID)
		

	def indicesToTriangleStrips2(self,indicesList):
		StartDirection = -1
		id=0
		f1 = indicesList[id]
		id+=1
		f2 = indicesList[id]
		FaceDirection = StartDirection
		while(True):
		#for m in range(len(indicesList)-2):
			id+=1
			f3 = indicesList[id]
			#print f3
			if (f3==0xFFFF):
				if id==len(indicesList)-1:break
				id+=1
				f1 = indicesList[id]
				id+=1
				f2 = indicesList[id]
				FaceDirection = StartDirection	 
			else:
				#f3 += 1
				FaceDirection *= -1
				if (f1!=f2) and (f2!=f3) and (f3!=f1):
					if FaceDirection > 0:						
						self.triangleList.append([(f1),(f2),(f3)])
						#self.matIDList.append(matID)
					else:
						self.triangleList.append([(f1),(f3),(f2)])
						#self.matIDList.append(matID)
					if self.DRAW==True: 
						f1,f2,f3	
				f1 = f2
				f2 = f3
			if id==len(indicesList)-1:break
			
def image2png(imagePath):
	if os.path.exists(imagePath)==True:
		cmd=Cmd()
		cmd.PNG=True	
		cmd.input=imagePath
		cmd.run()
	
				
def diffuse(blendMat,data):
		ext=data.diffuse.split('.')[-1]
		pngImage=data.diffuse#.replace('.'+ext,'.png
		#print pngImage
		#if os.path.exists(pngImage)==False:
		#if ext.lower()!='png':
		#	image2png(data.diffuse)
			#pngImage=data.diffuse.replace('.'+ext,'.png')
		if os.path.exists(pngImage)==True:
				img=Blender.Image.Load(pngImage)
				imgName=blendMat.name+'-d'
				img.setName(imgName)
				texname=blendMat.name+'-d'
				tex = Blender.Texture.New(texname)
				tex.setType('Image')
				tex.image = img 
				blendMat.setTexture(data.DIFFUSESLOT,tex,Blender.Texture.TexCo.UV,\
				Blender.Texture.MapTo.COL| Blender.Texture.MapTo.ALPHA)
				#print dir(blendMat.getTextures()[data.DIFFUSESLOT])	
				#blendMat.getTextures()[data.DIFFUSESLOT].mtAlpha=-1
		#else:
		#	if self.WARNING==True:
		#		print 'failed...',data.diffuse

				
def reflection(blendMat,data):
		if os.path.exists(data.reflection)==True:
			img=Blender.Image.Load(data.reflection)
			imgName=blendMat.name.replace('-mat-','-refl-')
			img.setName(imgName)
			texname=blendMat.name.replace('-mat-','-refl-')
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img 
			blendMat.setTexture(data.REFLECTIONSLOT,tex,Blender.Texture.TexCo.REFL,Blender.Texture.MapTo.COL)	
			mtextures = blendMat.getTextures() 
			mtex=mtextures[data.REFLECTIONSLOT]
			mtex.colfac=data.REFLECTIONSTRONG
		#else:
		#	if self.WARNING==True:
		#		print 'failed...',data.reflection

				
				
def alpha(blendMat,data):
		if os.path.exists(data.alpha)==True:
			img=Blender.Image.Load(data.alpha)
			imgName=blendMat.name+'-a'
			img.setName(imgName)
			texname=blendMat.name+'-a'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			#if data.RGBTRANSPARENT==True:
			tex.setImageFlags('CalcAlpha')
			
			tex.image = img 
			blendMat.setTexture(data.ALPHASLOT,tex,Blender.Texture.TexCo.UV,\
			Blender.Texture.MapTo.ALPHA)
			if blendMat.getTextures()[data.DIFFUSESLOT] is not None:
				blendMat.getTextures()[data.DIFFUSESLOT].tex.setImageFlags()
				blendMat.getTextures()[data.DIFFUSESLOT].mtAlpha=0
		
		
				
def trans(blendMat,data):
		if os.path.exists(data.trans)==True:
			transPath=GetBlackFromImage(data.trans)
			if os.path.exists(transPath)==True:
				img=Blender.Image.Load(transPath)
				imgName=blendMat.name+'-t'
				img.setName(imgName)
				texname=blendMat.name+'-t'
				tex = Blender.Texture.New(texname)
				tex.setType('Image')
				tex.setImageFlags('CalcAlpha')
				
				tex.image = img 
				blendMat.setTexture(data.ALPHASLOT,tex,Blender.Texture.TexCo.UV,\
				Blender.Texture.MapTo.ALPHA)
				if blendMat.getTextures()[data.DIFFUSESLOT] is not None:
					blendMat.getTextures()[data.DIFFUSESLOT].tex.setImageFlags()
		
			
def diffuse1(blendMat,data):#csp
		if os.path.exists(data.diffuse1)==True:
			img=Blender.Image.Load(data.diffuse1)
			imgName=blendMat.name+'-d1'
			img.setName(imgName)
			texname=blendMat.name+'-d1'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img 
			blendMat.setTexture(data.DIFFUSE1SLOT,tex,Blender.Texture.TexCo.UV,\
			Blender.Texture.MapTo.CSP|Blender.Texture.MapTo.SPEC) 
			
			mtex=blendMat.getTextures()[data.DIFFUSE1SLOT]
			mtex.blendmode=Blender.Texture.BlendModes.MULTIPLY
			blendMat.getTextures()[data.DIFFUSE1SLOT].mtSpec=-1 
			#mtex=blendMat.getTextures()[data.DIFFUSE1SLOT]
			#mtex.blendmode=Blender.Texture.BlendModes.ADD
		#else:
		#	if self.WARNING==True:
		#		print 'failed...',data.diffuse1
			
def diffuse2(blendMat,data):
		if os.path.exists(data.diffuse2)==True:
			img=Blender.Image.Load(data.diffuse2)
			imgName=blendMat.name+'-d2'
			img.setName(imgName)
			texname=blendMat.name+'-d2'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img 
			blendMat.setTexture(data.DIFFUSE2SLOT,tex,Blender.Texture.TexCo.UV,\
			Blender.Texture.MapTo.COL|Blender.Texture.MapTo.CSP)
			
			mtex=blendMat.getTextures()[data.DIFFUSE2SLOT]
			mtex.blendmode=Blender.Texture.BlendModes.MULTIPLY
		#else:
		#	if self.WARNING==True:
		#		print 'failed...',data.diffuse1
			
def normal(blendMat,data): 
		ext=data.normal.split('.')[-1]
		pngImage=data.normal#.replace('.'+ext,'.png')
		if os.path.exists(pngImage)==False:
		#if ext.lower()!='png':
			image2png(data.normal)
			#pngImage=data.normal.replace('.'+ext,'.png')
		if os.path.exists(pngImage)==True:
				img=Blender.Image.Load(pngImage)
				imgName=blendMat.name+'-n'
				img.setName(imgName)
				texname=blendMat.name+'-n'
				tex = Blender.Texture.New(texname)
				tex.setType('Image')
				tex.image = img 
				tex.setImageFlags('NormalMap')
				blendMat.setTexture(data.NORMALSLOT,tex,Blender.Texture.TexCo.UV,Blender.Texture.MapTo.NOR)
				blendMat.getTextures()[data.NORMALSLOT].norfac=data.NORMALSTRONG 
				blendMat.getTextures()[data.NORMALSLOT].mtNor=data.NORMALDIRECTION 
				blendMat.getTextures()[data.NORMALSLOT].size=data.NORMALSIZE
		#else:
		#	if self.WARNING==True:
		#		print 'failed...',data.normal 
			
def bump(blendMat,data): 
		ext=data.bump.split('.')[-1]
		pngImage=data.bump#.replace('.'+ext,'.png')
		if os.path.exists(pngImage)==False:
			image2png(data.bump)
		if os.path.exists(pngImage)==True:
				
				if os.path.exists(pngImage+'.png')==False:
					conv=bump2normal()
					conv.input=pngImage
					conv.output=pngImage+'.png'
					conv.filter=sobel
					conv.run()
				if os.path.exists(pngImage+'.png')==True:
				
				
					img=Blender.Image.Load(pngImage+'.png')
					imgName=blendMat.name+'-n'
					img.setName(imgName)
					texname=blendMat.name+'-n'
					tex = Blender.Texture.New(texname)
					tex.setType('Image')
					tex.image = img 
					tex.setImageFlags('NormalMap')
					blendMat.setTexture(data.NORMALSLOT,tex,Blender.Texture.TexCo.UV,Blender.Texture.MapTo.NOR)
					blendMat.getTextures()[data.NORMALSLOT].norfac=data.NORMALSTRONG 
					blendMat.getTextures()[data.NORMALSLOT].mtNor=data.NORMALDIRECTION 
					blendMat.getTextures()[data.NORMALSLOT].size=data.NORMALSIZE
		#else:
		#	if self.WARNING==True:
		#		print 'failed...',data.normal 
		
def specular(blendMat,data):
		ext=data.specular.split('.')[-1]
		pngImage=data.specular#.replace('.'+ext,'.png')
		if os.path.exists(pngImage)==False:
		#if ext.lower()!='png':
			image2png(data.specular)
			#pngImage=data.diffuse.replace('.'+ext,'.png')
		if os.path.exists(pngImage)==True:
		#if os.path.exists(data.specular)==True:
			img=Blender.Image.Load(data.specular)
			imgName=blendMat.name+'-s'
			img.setName(imgName)
			texname=blendMat.name+'-s'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img 
			blendMat.setTexture(data.SPECULARSLOT,tex,Blender.Texture.TexCo.UV,Blender.Texture.MapTo.CSP|Blender.Texture.MapTo.SPEC|Blender.Texture.MapTo.EMIT)	
			mtextures = blendMat.getTextures() 
			mtex=mtextures[data.SPECULARSLOT]
			mtex.neg=True
			mtex.blendmode=Blender.Texture.BlendModes.SUBTRACT
		#else:
		#	if self.WARNING==True:
		#		print 'failed...',data.specular			
			
def emit(blendMat,data):
		if os.path.exists(data.emit)==True:
			img=Blender.Image.Load(data.emit)
			imgName=blendMat.name+'-e'
			img.setName(imgName)
			texname=blendMat.name+'-e'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img 
			blendMat.setTexture(data.EMITSLOT,tex,Blender.Texture.TexCo.UV,Blender.Texture.MapTo.COL|Blender.Texture.MapTo.EMIT) 
			mtex=blendMat.getTextures()[data.EMITSLOT]
			mtex.blendmode=Blender.Texture.BlendModes.ADD 
			blendMat.getTextures()[data.EMITSLOT].mtEmit=-1 
			
def ao(blendMat,data):
		if os.path.exists(data.ao)==True:
			img=Blender.Image.Load(data.ao)
			imgName=blendMat.name+'-ao'
			img.setName(imgName)
			texname=blendMat.name+'-ao'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img 
			blendMat.setTexture(data.AOSLOT,tex,Blender.Texture.TexCo.UV,Blender.Texture.MapTo.COL) 
			mtex=blendMat.getTextures()[data.AOSLOT]
			mtex.blendmode=Blender.Texture.BlendModes.MULTIPLY
		#else:
		#	if self.WARNING==True:
		#		print 'failed...',data.ao	
			
def normal1(blendMat,data): 
		if os.path.exists(data.normal1)==True:
			img=Blender.Image.Load(data.normal1)
			imgName=blendMat.name+'-n1'
			img.setName(imgName)
			texname=blendMat.name+'-n1'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img 
			tex.setImageFlags('NormalMap')
			blendMat.setTexture(data.NORMAL1SLOT,tex,Blender.Texture.TexCo.UV,Blender.Texture.MapTo.NOR)
			blendMat.getTextures()[data.NORMAL1SLOT].norfac=data.NORMAL1STRONG 
			blendMat.getTextures()[data.NORMAL1SLOT].mtNor=data.NORMAL1DIRECTION 
			blendMat.getTextures()[data.NORMAL1SLOT].size=data.NORMAL1SIZE 
		##else:
		#	if self.WARNING==True:
		#		print 'failed...',data.normal1	
				
def normal2(blendMat,data): 
		if os.path.exists(data.normal2)==True:
			img=Blender.Image.Load(data.normal2)
			imgName=blendMat.name+'-n2'
			img.setName(imgName)
			texname=blendMat.name+'-n2'
			tex = Blender.Texture.New(texname)
			tex.setType('Image')
			tex.image = img 
			tex.setImageFlags('NormalMap')
			blendMat.setTexture(data.NORMAL2SLOT,tex,Blender.Texture.TexCo.UV,Blender.Texture.MapTo.NOR)
			blendMat.getTextures()[data.NORMAL2SLOT].norfac=data.NORMAL2STRONG 
			blendMat.getTextures()[data.NORMAL2SLOT].mtNor=data.NORMAL2DIRECTION 
			blendMat.getTextures()[data.NORMAL2SLOT].size=data.NORMAL2SIZE 
		#else:
		#	if self.WARNING==True:
		#		print 'failed...',data.normal2	
		
	
					
class Skin:
	def __init__(self):
		self.boneMap=[]
		self.IDStart=None
		self.IDCount=None
		self.skeleton=None
		self.skeletonFile=None
			

		
class Mat:
	def __init__(self):#0,1,2,3,4,5,6,7,
		self.name=None
		self.matrix=None
		self.BINDSKELETON=None
		self.ZTRANS=False
		self.RGBTRANSPARENT=False
		
		self.diffuse=None
		self.DIFFUSESLOT=0
		self.NORMALSLOT=1
		self.SPECULARSLOT=2
		self.AOSLOT=3
		self.NORMAL1SLOT=4
		self.NORMAL2SLOT=5
		self.DIFFUSE1SLOT=6
		self.DIFFUSE2SLOT=7
		self.REFLECTIONSLOT=8
		self.ALPHASLOT=8
		#self.RGBTRANSPARENTSLOT=8
		self.EMITSLOT=9
		
		self.diffuse1=None
		self.diffuse2=None
		self.alpha=None
		
		self.normal=None
		self.NORMALSTRONG=0.5
		self.NORMALDIRECTION=1
		self.NORMALSIZE=(1,1,1) 
		
		self.bump=None
		
		self.specular=None
		
		self.ao=None
		
		self.normal1=None
		self.NORMAL1STRONG=0.8
		self.NORMAL1DIRECTION=1
		self.NORMAL1SIZE=(15,15,15) 
		
		self.normal2=None
		self.NORMAL2STRONG=0.8
		self.NORMAL2DIRECTION=1
		self.NORMAL2SIZE=(15,15,15) 
		
		self.reflection=None
		self.REFLECTIONSTRONG=1.0
		
		self.emit=None
		
		#self.USEDTRIANGLES=[None,None]
		self.TRIANGLE=False
		self.TRISTRIP=False
		self.QUAD=False
		self.IDStart=None
		self.IDCount=None
		self.faceIDList=[]
		self.rgbCol=None
		self.rgbSpec=None
		
		r=random.randint(0,255)
		g=random.randint(0,255)
		b=random.randint(0,255)
		self.rgba=[r/255.0,g/255.0,b/255.0,1.0]
		
		self.trans=None
		
	def draw(self): 
		if self.name is None:
			self.name=str(ParseID())+'-mat-'+str(0)
		blendMat=Blender.Material.New(self.name)
		blendMat.diffuseShader=Blender.Material.Shaders.DIFFUSE_ORENNAYAR
		blendMat.specShader=Blender.Material.Shaders.SPEC_WARDISO
		blendMat.setRms(0.04)
		blendMat.shadeMode=Blender.Material.ShadeModes.CUBIC
		if self.ZTRANS==True:
			blendMat.mode |= Blender.Material.Modes.ZTRANSP
			blendMat.mode |= Blender.Material.Modes.TRANSPSHADOW
			blendMat.alpha = 0.0 
		if self.diffuse is not None:diffuse(blendMat,self)
		if self.reflection is not None:reflection(blendMat,self)
		if self.diffuse1 is not None:diffuse1(blendMat,self)
		if self.diffuse2 is not None:diffuse2(blendMat,self)
		if self.specular is not None:specular(blendMat,self)
		if self.normal is not None:normal(blendMat,self)
		if self.normal1 is not None:normal1(blendMat,self)
		if self.normal2 is not None:normal2(blendMat,self)
		if self.ao is not None:ao(blendMat,self)
		if self.alpha is not None:alpha(blendMat,self)	
		