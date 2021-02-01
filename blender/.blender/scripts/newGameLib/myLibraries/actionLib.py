import bpy
import Blender
		
class ActionBone:
	def	__init__(self):
		self.name=None
		self.posFrameList=[]
		self.rotFrameList=[]
		self.scaleFrameList=[]
		self.posKeyList=[]
		self.rotKeyList=[]
		self.scaleKeyList=[]
		self.matrixFrameList=[]
		self.matrixKeyList=[]
		
	
class Action:
	def __init__(self):
		self.frameCount=None
		self.name='action'
		self.skeleton='armature'
		self.boneList=[]
		self.ARMATURESPACE=False
		self.BONESPACE=False
		self.MIXSPACE=False
		self.FRAMESORT=False
		self.BONESORT=False
		self.UPDATE=True
		
	def boneNameList(self):
		if self.skeleton is not None:
			scene = bpy.data.scenes.active
			for object in scene.objects:
				if object.name==self.skeleton:
					self.boneNameList=object.getData().bones.keys()
		
		
	def setContext(self):
		scn = Blender.Scene.GetCurrent()
		context = scn.getRenderingContext()
		if self.frameCount is not None:
			context.eFrame = self.frameCount	
		
		
		
		
		
	def draw(self):
		scene = bpy.data.scenes.active
		skeleton=None
		if self.skeleton is not None:
			for object in scene.objects:
				if object.getType()=='Armature':
					if object.name==self.skeleton:				
						skeleton = object
		else:
			print 'WARNING: no armature'
		if skeleton is not None:			
			armature=skeleton.getData()
			pose = skeleton.getPose()
			action = Blender.Armature.NLA.NewAction(self.name)
			action.setActive(skeleton)
			scn = Blender.Scene.GetCurrent()
			timeList=[]
			
			if self.FRAMESORT is True:
				frameList=[]
				for m in range(len(self.boneList)):
					actionbone=self.boneList[m]
					for n in range(len(actionbone.posFrameList)):
						frame=actionbone.posFrameList[n]
						if frame not in frameList:
							frameList.append(frame)
					for n in range(len(actionbone.rotFrameList)):
						frame=actionbone.rotFrameList[n]
						if frame not in frameList:
							frameList.append(frame)
					for n in range(len(actionbone.matrixFrameList)):
						frame=actionbone.matrixFrameList[n]
						if frame not in frameList:
							frameList.append(frame)
										
				for k in range(len(frameList)):
					frame=sorted(frameList)[k]
					for m in range(len(self.boneList)):
						actionbone=self.boneList[m]
						name=actionbone.name
						pbone=pose.bones[name]
						if pbone is not None:
							for n in range(len(actionbone.posFrameList)):
								if frame==actionbone.posFrameList[n]:
									timeList.append(frame)
									poskey=actionbone.posKeyList[n]
									bonematrix=poskey#TranslationMatrix(Vector(poskey))#.resize4x4()
									if self.ARMATURESPACE is True:
										pbone.poseMatrix=bonematrix
										pbone.insertKey(skeleton, frame,\
											[Blender.Object.Pose.LOC],True)
										if self.UPDATE==True:pose.update()
									if self.BONESPACE is True:
										if pbone.parent:		
											pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
										else:
											pbone.poseMatrix=bonematrix
										pbone.insertKey(skeleton, frame,\
											[Blender.Object.Pose.LOC],True)
										if self.UPDATE==True:pose.update()
										
									
									
							for n in range(len(actionbone.rotFrameList)):
								if frame==actionbone.rotFrameList[n]:
									timeList.append(frame)
									rotkey=actionbone.rotKeyList[n]
									bonematrix=rotkey
									if self.ARMATURESPACE is True:
										pbone.poseMatrix=bonematrix
										pbone.insertKey(skeleton, frame,\
											[Blender.Object.Pose.ROT],True)
										if self.UPDATE==True:pose.update()
									if self.BONESPACE is True:
										if pbone.parent:		
											pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
										else:
											pbone.poseMatrix=bonematrix
										pbone.insertKey(skeleton, frame,\
											[Blender.Object.Pose.ROT],True)
										if self.UPDATE==True:pose.update()
											
							for n in range(len(actionbone.matrixFrameList)):
								if frame==actionbone.matrixFrameList[n]:
									timeList.append(frame)
									matrix=actionbone.matrixKeyList[n]
									if self.ARMATURESPACE is True:
										pbone.poseMatrix=matrix
										pbone.insertKey(skeleton, 1+frame,\
											[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
											#[Blender.Object.Pose.LOC],True)
										if self.UPDATE==True:pose.update()
									if self.BONESPACE is True:
										if pbone.parent:		
											pbone.poseMatrix=matrix*pbone.parent.poseMatrix
										else:
											pbone.poseMatrix=skeleton.matrixWorld*matrix
										pbone.insertKey(skeleton, 1+frame,\
											[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
										if self.UPDATE==True:pose.update()
										
									if self.MIXSPACE is True:
										if pbone.parent:		
											pbone.poseMatrix=matrix*pbone.parent.poseMatrix
											pbone.quat=matrix.rotationPart().toQuat()
										else:
											pbone.poseMatrix=skeleton.matrixWorld*matrix
											pbone.quat=matrix.rotationPart().toQuat()
										pbone.insertKey(skeleton, 1+frame,\
											[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
										if self.UPDATE==True:pose.update()
					#pose.update()
				
			elif self.BONESORT is True:
				#print 'co jest kurwa mac'
				for m in range(len(self.boneList)):
					actionbone=self.boneList[m]
					name=actionbone.name
					pbone=pose.bones[name]
					Blender.Window.RedrawAll()
					#print name
					
					
					if pbone is not None:
						#matrix=armature.bones[name].matrix['ARMATURESPACE']
						pbone.insertKey(skeleton,0,[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
						pose.update()
						
						for n in range(len(actionbone.posFrameList)):
							frame=actionbone.posFrameList[n]
							timeList.append(frame)
							poskey=actionbone.posKeyList[n]
							bonematrix=poskey#TranslationMatrix(Vector(poskey))#.resize4x4()
							if self.ARMATURESPACE is True:
								pbone.poseMatrix=bonematrix
								#pbone.loc=bonematrix
								pbone.insertKey(skeleton, 1+frame,\
									[Blender.Object.Pose.LOC],True)
								if self.UPDATE==True:pose.update()
							if self.BONESPACE is True:
								if pbone.parent:		
									pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
									#pbone.loc=bonematrix*pbone.parent.poseMatrix+pbone.parent.head
								else:
									pbone.poseMatrix=bonematrix
									#pbone.loc=bonematrix
								pbone.insertKey(skeleton, 1+frame,\
									[Blender.Object.Pose.LOC],True)
								if self.UPDATE==True:pose.update()
								
								
						for n in range(len(actionbone.rotFrameList)):
							frame=actionbone.rotFrameList[n]
							timeList.append(frame)
							rotkey=actionbone.rotKeyList[n]
							bonematrix=rotkey
							if self.ARMATURESPACE is True:
								pbone.poseMatrix=bonematrix
								#pbone.quat=bonematrix
								pbone.insertKey(skeleton, 1+frame,\
									[Blender.Object.Pose.ROT],True)
								if self.UPDATE==True:pose.update()
							if self.BONESPACE is True:
								if pbone.parent:		
									pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
								else:
									pbone.poseMatrix=bonematrix
									#pbone.quat=bonematrix
								pbone.insertKey(skeleton, 1+frame,\
									[Blender.Object.Pose.ROT],True)
								if self.UPDATE==True:pose.update()
								
						for n in range(len(actionbone.matrixFrameList)):
							frame=actionbone.matrixFrameList[n]
							timeList.append(frame)
							matrixkey=actionbone.matrixKeyList[n]
							bonematrix=matrixkey
							if self.ARMATURESPACE is True:
								pbone.poseMatrix=skeleton.matrixWorld*bonematrix
								pbone.insertKey(skeleton, 1+frame,\
									[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
								if self.UPDATE==True:pose.update()
							if self.BONESPACE is True:
								if pbone.parent:		
									pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
								else:
									pbone.poseMatrix=bonematrix
								pbone.insertKey(skeleton, 1+frame,\
									[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
								if self.UPDATE==True:pose.update()
										
							if self.MIXSPACE is True:
								if pbone.parent:		
									pbone.poseMatrix=bonematrix*pbone.parent.poseMatrix
									pbone.quat=bonematrix.rotationPart().toQuat()
								else:
									pbone.poseMatrix=skeleton.matrixWorld*bonematrix
									pbone.quat=bonematrix.rotationPart().toQuat()
								pbone.insertKey(skeleton, 1+frame,\
									[Blender.Object.Pose.ROT,Blender.Object.Pose.LOC],True)
								if self.UPDATE==True:pose.update()
						#pose.update()
				#print timeList	
			else:
				print 'WARNING: missing BONESORT or FRAMESORT'
			#print timeList	
			if len(timeList)>0:
				print max(map(int,timeList))	
				self.frameCount=max(map(int,timeList))
						
