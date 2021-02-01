# -*- coding: utf-8 -*-
import newGameLib
from newGameLib import *
import Blender
import bpy
import os
import build_args_parser # put it into .blend/scripts/
################################################
#BINDPOSE=0
BINDPOSE=1
################################################
global build_args

class Node:
	def __init__(self):
		self.name=None
		self.children=[]
		self.osgChildren=[]
		self.offset=None
		self.start=None
		self.end=None
		self.header=''
		self.data=''
	
class Yson:
	def __init__(self):
		self.input=None
		self.filename=None
		self.root=Node()
		self.log=False
	def parse(self):
		global offset,string,txt
		if self.filename is not None:
			file=open(self.filename,'rb')
			self.input=file.read().replace('\x20','').replace('\x0A','')		
		
			line=self.input
			if self.log==True:txt=open(self.filename+'.ys','w')
			
			if line is not None and len(line)>0:
				offset=0
				n=0
				string=[]
				if self.input[offset]=='{':
					if self.log==True:
						txt.write('\n')
						txt.write(' '*n+'header:'+str(None))
						txt.write(' { '+str(offset))
						txt.write(' '*(n+4))
				if self.input[offset]=='[':
					if self.log==True:
						txt.write('\n')
						txt.write(' '*n+'header:'+str(None))
						txt.write(' [ '+str(offset))
						txt.write(' '*(n+4))
				self.tree(self.root,n)
				if self.log==True:
					txt.write(' '*n)
				print round(100*offset/float(len(self.input)),3),'procent'
				
			file.close()	
			
		if self.log==True:txt.close()

	def getTree(self,parent,list,key):
		for child in parent.children:
			if key in child.header:
				list.append(child)
			self.getTree(child,list,key)
			
		

	def values(self,data,type):
		list={}
		A=data.split(',')
		if type==':':
			for a in A:
				if ':' in a:
					c=0
					alist=[]
					string=''
					#print a
					for b in a:
						if b=='"' and c==0:
							#string+=b
							if len(string)>0:alist.append(string)
							string=''
							string+=b
							c=1
						elif b=='"' and c==1:
							string+=b
							if len(string)>0:alist.append(string)
							string=''
							c=0
						elif b==':':
							#list.append(b)
							#string=''
							#c=0
							pass
						else:string+=b
					if len(string)>0:alist.append(string)
					if len(alist)==2:	
						list[alist[0]]=alist[1]				
									
						
							
					#if a.count(':')>1:
		if type=='f':
			list=map(float,A)
		if type=='i':
			list=map(int,A)
		if type=='s':
			list=A
		return list	

	def getValue(self,values,name,type=None):
		if name in values:
			if type=='"f"':
				return float(values[name].split('"')[1])
			elif type=='"i"':
				return int(values[name].split('"')[1])
			elif type=='i':
				return int(values[name])
			elif type=='""':
				return values[name].split('"')[1]
			else:
				return values[name]
		else:
			return None
		
	def get(self,node,key):		
		list=[]
		self.getTree(node,list,key)
		if len(list)>0:
			return list	
		else:
			return None
			
	def tree(self,parentNode,n):
		global offset,string
		n+=4
		offset+=1
		while(True):	
			if	offset>=len(self.input):break
			value=self.input[offset]
			if value=='}':
				if self.log==True:
					txt.write('\n')
					if len(string)>0:
						txt.write(' '*n+'data:'+self.input[string[0]:offset])	
					else:	
						txt.write(' '*n+'data:None')				
					txt.write('\n'+' '*n+' } '+str(offset))
				if len(string)>0:	
					parentNode.data=self.input[string[0]:offset]
				string=[]
				offset+=1			
				break
			
			elif value=='{':
				if self.log==True:
					txt.write('\n')
					if len(string)>0:
						txt.write(' '*n+'header:'+self.input[string[0]:offset])	
					else:	
						txt.write(' '*n+'header:None')				
					txt.write(' { '+str(offset))
					txt.write(' '*(n+4))
				#print round(100*offset/float(len(self.input)),3),'procent'
				node=Node()
				parentNode.children.append(node)
				node.offset=offset
				if len(string)>0:
					node.header=self.input[string[0]:offset]
				string=[]
				self.tree(node,n)
				if self.log==True:
					txt.write(' '*n)
				
			elif value==']':
				if len(string)>0:
					parentNode.data=self.input[string[0]:offset]
				
				if self.log==True:
					txt.write('\n')
					if len(string)>0:
						txt.write(' '*n+'data:'+self.input[string[0]:offset]+'\n')	
					else:	
						txt.write(' '*n+'data:None')							
					txt.write(' '*n+' ] '+str(offset))
					
				offset+=1
				string=[]
				break
			
			elif value=='[':
				if self.log==True:
					txt.write('\n')
					if len(string)>0:
						txt.write(' '*n+'header:'+self.input[string[0]:offset])
					else:	
						txt.write(' '*n+'header:None')
					txt.write(' [ '+str(offset))
					txt.write(' '*(n+4))
				#print round(100*offset/float(len(self.input)),3),'procent'
				node=Node()
				parentNode.children.append(node)
				node.offset=offset
				node.name=string
				if len(string)>0:
					node.header=self.input[string[0]:offset]
				else:
					node.header=''
				string=[]
				self.tree(node,n)
				if self.log==True:
					txt.write(' '*n)
			else:			
				#string+=value
				if len(string)==0:
					string.append(offset)
				offset+=1
					
	
		
	
	
def decodeVarint(g,offset,size,type):
	g.seek(offset)
	n=[0]*size
	a=0
	s=0	
	while(a!=size):
		shift = 0
		result = 0
		while True:
			byte = g.B(1)[0]
			result |= (byte & 127) << shift
			shift += 7
			if not (byte & 0x80):break			
		n[a]=result		
		a+=1
	if type[0]!='U':
		l=0
		while(l<size):
			h=n[l]
			n[l]=h>>1^-(1&h)
			l+=1
	return n
		
	
		
def decodeDelta(t,e):
	i=e|0
	n=len(t)
	if i>=len(t):r=None
	else:r=t[i]
	a=i+1
	while(a<n):
		s=t[a]
		r=t[a]=r+(s>>1^-(1&s))
		a+=1
	return t	


def decodeImplicit(input,n):
	IMPLICIT_HEADER_LENGTH=3
	IMPLICIT_HEADER_MASK_LENGTH=1
	IMPLICIT_HEADER_PRIMITIVE_LENGTH=0
	IMPLICIT_HEADER_EXPECTED_INDEX=2
	highWatermark=2
	
	t=input
	e=[0]*t[IMPLICIT_HEADER_PRIMITIVE_LENGTH]
	a=t[IMPLICIT_HEADER_EXPECTED_INDEX]
	s=t[IMPLICIT_HEADER_MASK_LENGTH]
	o=t[IMPLICIT_HEADER_LENGTH:s+IMPLICIT_HEADER_LENGTH]
	r=highWatermark
	u=32*s-len(e)
	l=1<<31
	h=0	
	while(h<s):
		c=o[h]
		d=32
		p=h*d
		if h==s-1:f=u
		else:f=0
		g1=f
		while(g1<d):
			if c&l>>g1:
				e[p]=t[n]
				n+=1	
			else:
				if r:
					e[p]=a
				else:
					e[p]=a
					a+=1			
			g1+=1
			p+=1
		h+=1
	return e		
	
	
def decodeWatermark(t,e,i):
	n=i[0]
	r=len(t)
	a=0
	while(a<r):
		s=n-t[a]
		e[a]=s
		if n<=s:n=s+1
		a+=1
	return e,n

	
def getIndices(itemsize,size,offset,type,g,mode,magic):
	if type!="Uint8Array":bytes=decodeVarint(g,offset,size*itemsize,type)
	else:
		g.seek(offset)
		bytes=list(g.B(size*itemsize))		
	#write(log,[magic],0)
	#write(log,bytes,0)		
	
	IMPLICIT_HEADER_LENGTH=3
	IMPLICIT_HEADER_MASK_LENGTH=1
	IMPLICIT_HEADER_PRIMITIVE_LENGTH=0
	IMPLICIT_HEADER_EXPECTED_INDEX=2
	highWatermark=2
	

		
	if mode=='"TRIANGLE_STRIP"':
			k=IMPLICIT_HEADER_LENGTH+bytes[IMPLICIT_HEADER_MASK_LENGTH]
			bytes=decodeDelta(bytes,k)	
			#write(log,[magic,k],0)	
			#write(log,bytes,0)		
			bytes=decodeImplicit(bytes,k)
			#write(log,[magic,k],0)	
			#write(log,bytes,0)			
			i=[magic]	
			bytes,magic=decodeWatermark(bytes,bytes,i)
			#write(log,[magic],0)	
			#write(log,bytes,0)	
			
	elif mode=='"TRIANGLES"':
			k=0
			bytes=decodeDelta(bytes,k)
			#write(log,[magic],0)	
			#write(log,bytes,0)			
			i=[magic]	
			bytes,magic=decodeWatermark(bytes,bytes,i)
			#write(log,[magic],0)	
			#write(log,bytes,0)	
		
		
		
		
	return magic,bytes
	
	
def decodePredict(indices,input,itemsize):	
	t=input	
	if len(indices)>0:
		t=input	
		e=itemsize
		i=indices	
		n=len(t)/e
		r=[0]*n
		a=len(i)-1
		r[i[0]]=1
		r[i[1]]=1
		r[i[2]]=1	
		s=2
		while(s<a):
			o=s-2
			u=i[o]
			l=i[o+1]
			h=i[o+2]
			c=i[o+3]
			if 1!=r[c]:
				r[c]=1
				u*=e
				l*=e
				h*=e
				c*=e			
				d=0
				while(d<e):
					t[c+d]=t[c+d]+t[l+d]+t[h+d]-t[u+d]
					d+=1
			s+=1
	return t

	
def etap1(input,ItemSize):
	n=len(input)/ItemSize
	r=0
	output=[0]*len(input)
	while(r<n):
		a=r*ItemSize
		s=0
		while(s<ItemSize):
			output[a+s]=input[r+n*s]
			s+=1	
		r+=1
	return output	
	
def etap2(input,ItemSize,atributes):
	i=[atributes['"bx"'],atributes['"by"'],atributes['"bz"']]
	n=[atributes['"hx"'],atributes['"hy"'],atributes['"hz"']]
	#start=[atributes['"ox"'],atributes['"oy"'],atributes['"oz"']]
	

	a=len(input)/ItemSize
	s=0
	output=[0]*len(input)
	while(s<a):
		o=s*ItemSize
		u=0
		while(u<ItemSize):
			output[o+u]=i[u]+input[o+u]*n[u];
			u+=1	
		s+=1
		
	#start.extend(output)
	#start[0]=atributes['"ot"']	
	return output	
	
	
	
	
def etap3(input,ItemSize):
	i=ItemSize|1
	n=1
	r=len(input)/i
	while(n<r):
		a=(n-1)*i
		s=n*i
		o=0
		while(o<i):			
			input[s+o]+=input[a+o]
			o+=1	
		n+=1
	return input
	
def etap4(input):
	e=1
	i=len(input)/4
	while(e<i):
		n=4*(e-1)
		r=4*e
		a=input[n]
		s=input[n+1]
		o=input[n+2]
		u=input[n+3]
		l=input[r]
		h=input[r+1]
		c=input[r+2]
		d=input[r+3]
		input[r]=a*d+s*c-o*h+u*l
		input[r+1]=-a*c+s*d+o*l+u*h
		input[r+2]=a*h-s*l+o*d+u*c
		input[r+3]=-a*l-s*h-o*c+u*d
		e+=1
	return	input
	


def int3float4(input,atributes,ItemSize):
	c=4
	d=atributes['"epsilon"']
	p=int(atributes['"nphi"'])
	e=[0]*len(input)*4
	i=1.57079632679
	n=6.28318530718
	r=3.14159265359
	a=.01745329251
	s=.25
	o=720
	u=832
	l=47938362584151635e-21
	h={}
	f=True
	
	d=d or s
	p=p or o
	g=math.cos(d*a)
	m=0
	v=0
	_=[]
	
	v=(p+1)*(u+1)*3
	_=[None]*v
	
	b=r/float(p-1)
	x=i/float(p-1)
	
	if f:y=3
	else:y=2
		
		
	m=0
	v=len(input)/y
	while(m<v):
		A=m*c
		S=m*y
		C=input[S]
		w=input[S+1]
		if c==0:
			if f==0:
				if (C&-1025)!=4:		
					e[A+3]=-1
				else:
					e[A+3]=1
		M=None
		T=None
		E=None
		I=3*(C+p*w)		
		M=_[I]
		if	M==None:				
			N=C*b
			k=cos(N)
			F=sin(N)
			N+=x
			D=(g-k*cos(N))/float(max(1e-5,F*sin(N)))
			if D>1:D=1
			else:
				if D<-1:D=-1
			P=w*n/float(math.ceil(r/float(max(1e-5,math.acos(D)))))
			M=_[I]=F*math.cos(P)
			T=_[I+1]=F*math.sin(P)
			E=_[I+2]=k
		else: 
			T=_[I+1]
			E=_[I+2]
		if f:
			R=input[S+2]*l
			O=math.sin(R)
			e[A]=O*M
			e[A+1]=O*T
			e[A+2]=O*E
			e[A+3]=math.cos(R)
			#write(log,[A,e[A],e[A+1],e[A+2],e[A+3]],0)
		else: 
			e[A]=M
			e[A+1]=T
			e[A+2]=E
		m+=1
	
	
	
	
	#write(log,_,0)
	return e	


def getSplitName(name,what,which):
	a=None
	if what in name:
		a=''
		splits=name.split(what)
		if which<0:
			num=len(splits)+which-1
		else:
			num=which
		if num<0:
			a=name
		else:		
			if which<len(splits):			
				for m in range(num):
					a+=splits[m]+what
				a+=splits[num]
			else:
				a=name		
	return a	
		

def getAnimation(ys,A,n):
	action=Action()
	action.ARMATURESPACE=True
	action.BONESORT=True
	action.skeleton=skeleton.name
	n+=4
	Channels=ys.get(A,'"Channels"')
	boneList={}
	if Channels:
		values=ys.values(Channels[0].header,':')
		Name=ys.getValue(values,'"Name"')
		action.name=Name
		write(log,[Name],n)
		
		for a in  Channels[0].children:
			write(log,['Bone'],n)
			Vec3LerpChannel=ys.get(a,'"osgAnimation.Vec3LerpChannel"')
			bone=None
			if Vec3LerpChannel:
				KeyFrames=ys.get(a,'"KeyFrames"')
				if KeyFrames:
					values=ys.values(KeyFrames[0].header,':')
					Name=ys.getValue(values,'"Name"')
					TargetName=ys.getValue(values,'"TargetName"','""')
					write(log,['Vec3LerpChannel:',Name,'TargetName:',TargetName],n+4)
					name=getSplitName(TargetName,'_',-1)
					if Name=='"translate"':
						if name in boneIndeksList:
							name=boneIndeksList[name]
							if name not in boneList.keys():
								bone=ActionBone()
								action.boneList.append(bone)
								bone.name=name
								boneList[name]=bone
							bone=boneList[name]
						
						
						Key=ys.get(a,'"Key"')
						if Key:
							values=ys.values(Key[0].data,':')
							ItemSize=ys.getValue(values,'"ItemSize"','i')						
							Float32Array=ys.get(Key[0],'"Float32Array"')
							if Float32Array:
								values=ys.values(Float32Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=ys.getValue(values,'"Size"')
								Offset=ys.getValue(values,'"Offset"')
								write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)
								path=os.path.dirname(input.filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(int(Offset))
									for m in range(int(Size)):
										value=g.f(ItemSize)
										write(log,value,n+8)
										if bone:
											boneMatrix=skeleton.object.getData().bones[bone.name].matrix['ARMATURESPACE']
											bone.posKeyList.append(boneMatrix*VectorMatrix(value))
									file.close()
						
						Time=ys.get(a,'"Time"')
						if Time:
							values=ys.values(Time[0].data,':')
							ItemSize=ys.getValue(values,'"ItemSize"','i')						
							Float32Array=ys.get(Time[0],'"Float32Array"')
							if Float32Array:
								values=ys.values(Float32Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=ys.getValue(values,'"Size"')
								Offset=ys.getValue(values,'"Offset"')
								write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)
								path=os.path.dirname(input.filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(int(Offset))
									for m in range(int(Size)):
										value=g.f(ItemSize)
										if ItemSize==1:value=value[0]
										#write(log,[value],n+8)
										if bone:bone.posFrameList.append(int(value*33))
									file.close()
					
									
			Vec3LerpChannelCompressedPacked=ys.get(a,'"osgAnimation.Vec3LerpChannelCompressedPacked"')
			if Vec3LerpChannelCompressedPacked:
			
				atributes={}
				UserDataContainer=ys.get(Vec3LerpChannelCompressedPacked[0],'"UserDataContainer"')
				if UserDataContainer:
					Values=ys.get(UserDataContainer[0],'"Values"')
					if Values:
						for child in Values[0].children:
							values=ys.values(child.data,':')
							Name=ys.getValue(values,'"Name"')
							Value=ys.getValue(values,'"Value"','"f"')
							#write(log,[Name,Value],n+4)
							atributes[Name]=Value
				
				KeyFrames=ys.get(a,'"KeyFrames"')
				if KeyFrames:
					values=ys.values(KeyFrames[0].header,':')
					Name=ys.getValue(values,'"Name"')
					TargetName=ys.getValue(values,'"TargetName"','""')
					write(log,['Vec3LerpChannelCompressedPacked:',Name,'TargetName:',TargetName],n+4)
					name=getSplitName(TargetName,'_',-1)
					if Name=='"translate"':
						if name in boneIndeksList:
							name=boneIndeksList[name]
							if name not in boneList.keys():
								bone=ActionBone()
								action.boneList.append(bone)
								bone.name=name
								boneList[name]=bone
							bone=boneList[name]
						
						Key=ys.get(a,'"Key"')
						if Key:
							values=ys.values(Key[0].data,':')
							ItemSize=int(ys.getValue(values,'"ItemSize"'))						
							Uint16Array=ys.get(Key[0],'"Uint16Array"')
							type="Uint16Array"
							if Uint16Array:
								values=ys.values(Uint16Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=int(ys.getValue(values,'"Size"'))
								Offset=int(ys.getValue(values,'"Offset"'))
								Encoding=ys.getValue(values,'"Encoding"')
								write(log,[File,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'ItemSize:',ItemSize],n+4)
								path=os.path.dirname(input.filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)
									
									list=decodeVarint(g,Offset,Size*ItemSize,type)
									list1=etap1(list,ItemSize)
									out=etap2(list1,ItemSize,atributes)
									list2=[atributes['"ox"'],atributes['"oy"'],atributes['"oz"']]
									list2.extend(out)
									list3=etap3(list2,ItemSize)
									for m in range(Size+1):
										value=list3[m*3:m*3+3]
										write(log,value,n+8)
										if bone:
											boneMatrix=skeleton.object.getData().bones[bone.name].matrix['ARMATURESPACE']
											bone.posKeyList.append(boneMatrix*VectorMatrix(value))
									file.close()
						
						Time=ys.get(a,'"Time"')
						if Time:
							values=ys.values(Time[0].data,':')
							ItemSize=ys.getValue(values,'"ItemSize"','i')						
							Float32Array=ys.get(Time[0],'"Float32Array"')
							if Float32Array:
								values=ys.values(Float32Array[0].data,':')
								File=ys.getValue(values,'"File"')
								Size=ys.getValue(values,'"Size"','i')
								Offset=ys.getValue(values,'"Offset"','i')
								write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)
								path=os.path.dirname(input.filename)+os.sep+File.split('"')[1].split('.gz')[0]
								if os.path.exists(path):
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(int(Offset))
									list=g.f(Size*ItemSize)
									list1=etap1(list,ItemSize)
									#out=etap2(list1,ItemSize,atributes)
									list2=[atributes['"ot"']]
									list2.extend(list1)
									list3=etap3(list2,ItemSize)
									#write(log,list3,0)
									for m in range(Size+1):
										value=list3[m]
										if bone:bone.posFrameList.append(int(value*33))
									file.close()
					
					
					
			QuatSlerpChannel=ys.get(a,'"osgAnimation.QuatSlerpChannel"')
			if QuatSlerpChannel:
				KeyFrames=ys.get(a,'"KeyFrames"')
				if KeyFrames:
					values=ys.values(KeyFrames[0].header,':')
					Name=ys.getValue(values,'"Name"')
					TargetName=ys.getValue(values,'"TargetName"','""')
					write(log,['QuatSlerpChannel:',Name,'TargetName:',TargetName],n+4)
					name=getSplitName(TargetName,'_',-1)
					if name in boneIndeksList:
						name=boneIndeksList[name]
						if name not in boneList.keys():
							bone=ActionBone()
							action.boneList.append(bone)
							bone.name=name
							boneList[name]=bone
						bone=boneList[name]
					
					
					
					Key=ys.get(a,'"Key"')
					if Key:
						values=ys.values(Key[0].data,':')
						ItemSize=ys.getValue(values,'"ItemSize"')						
						Float32Array=ys.get(Key[0],'"Float32Array"')
						if Float32Array:
							values=ys.values(Float32Array[0].data,':')
							File=ys.getValue(values,'"File"')
							Size=ys.getValue(values,'"Size"')
							Offset=ys.getValue(values,'"Offset"')
							write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)
							path=os.path.dirname(input.filename)+os.sep+File.split('"')[1].split('.gz')[0]
							if os.path.exists(path):
								file=open(path,'rb')
								g=BinaryReader(file)
								g.seek(int(Offset))
								for m in range(int(Size)):
									value=g.f(4)
									value=Quaternion(value)
									if bone:
										boneMatrix=skeleton.object.getData().bones[bone.name].matrix['ARMATURESPACE']
										bone.rotKeyList.append(boneMatrix*QuatMatrix(value).resize4x4())
								file.close()
					
					Time=ys.get(a,'"Time"')
					if Time:
						values=ys.values(Time[0].data,':')
						ItemSize=ys.getValue(values,'"ItemSize"','i')						
						Float32Array=ys.get(Time[0],'"Float32Array"')
						if Float32Array:
							values=ys.values(Float32Array[0].data,':')
							File=ys.getValue(values,'"File"')
							Size=ys.getValue(values,'"Size"')
							Offset=ys.getValue(values,'"Offset"')
							write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)
							path=os.path.dirname(input.filename)+os.sep+File.split('"')[1].split('.gz')[0]
							if os.path.exists(path):
								file=open(path,'rb')
								g=BinaryReader(file)
								g.seek(int(Offset))
								for m in range(int(Size)):
									value=g.f(ItemSize)
									if ItemSize==1:value=value[0]
									if bone:bone.rotFrameList.append(int(value*33))
								file.close()
					
									
			QuatSlerpChannelCompressedPacked=ys.get(a,'"osgAnimation.QuatSlerpChannelCompressedPacked"')
			if QuatSlerpChannelCompressedPacked:
			
			
				atributes={}
				UserDataContainer=ys.get(QuatSlerpChannelCompressedPacked[0],'"UserDataContainer"')
				if UserDataContainer:
					Values=ys.get(UserDataContainer[0],'"Values"')
					if Values:
						for child in Values[0].children:
							values=ys.values(child.data,':')
							Name=ys.getValue(values,'"Name"')
							Value=ys.getValue(values,'"Value"','"f"')
							#write(log,[Name,Value],n+4)
							atributes[Name]=Value
			
				KeyFrames=ys.get(a,'"KeyFrames"')
				if KeyFrames:
					values=ys.values(KeyFrames[0].header,':')
					Name=ys.getValue(values,'"Name"')
					TargetName=ys.getValue(values,'"TargetName"','""')
					write(log,['QuatSlerpChannelCompressedPacked:',Name,'TargetName:',TargetName],n+4)
					name=getSplitName(TargetName,'_',-1)
					if name in boneIndeksList:
						name=boneIndeksList[name]
						if name not in boneList.keys():
							bone=ActionBone()
							action.boneList.append(bone)
							bone.name=name
							boneList[name]=bone
						bone=boneList[name]
						
					Key=ys.get(a,'"Key"')
					if Key:
						values=ys.values(Key[0].data,':')
						ItemSize=int(ys.getValue(values,'"ItemSize"'))						
						Uint16Array=ys.get(Key[0],'"Uint16Array"')
						type="Uint16Array"
						if Uint16Array:
							values=ys.values(Uint16Array[0].data,':')
							File=ys.getValue(values,'"File"')
							Size=int(ys.getValue(values,'"Size"'))
							Offset=int(ys.getValue(values,'"Offset"'))
							Encoding=ys.getValue(values,'"Encoding"')
							write(log,[File,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'ItemSize:',ItemSize],n+4)
							path=os.path.dirname(input.filename)+os.sep+File.split('"')[1].split('.gz')[0]
							if os.path.exists(path):
								file=open(path,'rb')
								g=BinaryReader(file)
								
								list=decodeVarint(g,Offset,Size*ItemSize,type)
								#write(log,list,0)
								list1=etap1(list,ItemSize)
								#write(log,list1,0)
								
								list2=int3float4(list1,atributes,ItemSize)								
								#write(log,list2,0)
								list3=[atributes['"ox"'],atributes['"oy"'],atributes['"oz"'],atributes['"ow"']]
								list3.extend(list2)
								list4=etap4(list3)
								#write(log,list4,0)
								
								for m in range(Size+1):
									value=list4[m*4:m*4+4]									
									value=Quaternion(value)
									#write(log,value,n+8)
									if bone:
										boneMatrix=skeleton.object.getData().bones[bone.name].matrix['ARMATURESPACE']
										##bone.rotKeyList.append((boneMatrix.rotationPart()*QuatMatrix(value)).resize4x4())
										bone.rotKeyList.append(boneMatrix*QuatMatrix(value).resize4x4())
								file.close()
					
					Time=ys.get(a,'"Time"')
					if Time:
						values=ys.values(Time[0].data,':')
						ItemSize=ys.getValue(values,'"ItemSize"','i')						
						Float32Array=ys.get(Time[0],'"Float32Array"')
						if Float32Array:
							values=ys.values(Float32Array[0].data,':')
							File=ys.getValue(values,'"File"')
							Size=ys.getValue(values,'"Size"','i')
							Offset=ys.getValue(values,'"Offset"','i')
							write(log,[File,'Size:',Size,'Offset:',Offset,'ItemSize:',ItemSize],n+4)
							path=os.path.dirname(input.filename)+os.sep+File.split('"')[1].split('.gz')[0]
							if os.path.exists(path):
								file=open(path,'rb')
								g=BinaryReader(file)
								g.seek(int(Offset))
								list=g.f(Size*ItemSize)
								list1=etap1(list,ItemSize)
								#out=etap2(list1,ItemSize,atributes)
								list2=[atributes['"ot"']]
								list2.extend(list1)
								list3=etap3(list2,ItemSize)
								#write(log,list3,0)
								for m in range(Size+1):
									value=list2[m]
									if bone:bone.rotFrameList.append(int(value*33))
								file.close()
				
			if bone:	
				print name,bone.name
				
	action.draw()
	action.setContext()	
				
def getPrimitiveSetList(ys,PrimitiveSetList,n):
	global magic
	mode=None
	magic=0
	indiceArray=[]
	for child in PrimitiveSetList[0].children:
		for b in child.children:					
			if '"DrawElementsUInt"' in b.header:			
				values=ys.values(b.data,':')
				mode=values['"Mode"']			
				Size=None
				Offset=None
				Encoding=None
				ItemSize=None
				type=None
				if mode!='"LINES"':
					Indices=ys.get(b,'"Indices"')
					if Indices:
						values=ys.values(Indices[0].data,':')
						ItemSize=ys.getValue(values,'"ItemSize"','i')
						Uint32Array=ys.get(Indices[0],'"Uint32Array"')
						type="Uint32Array"
						print "DrawElementsUInt",type
						if Uint32Array:
							values=ys.values(Uint32Array[0].data,':')
							Size=ys.getValue(values,'"Size"','i')
							Offset=ys.getValue(values,'"Offset"','i')
							Encoding=ys.getValue(values,'"Encoding"','""')
							write(log,['Indice:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'magic:',magic],n)
							if Encoding=='varint':
								path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
								if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
								if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
								if os.path.exists(path)==True:
									file=open(path,'rb')
									g=BinaryReader(file)
									magic,indiceList=getIndices(ItemSize,Size,Offset,type,g,mode,magic)
									indiceArray.append([indiceList,mode])
									file.close()
				else:
					print 'LINES'
					
			if '"DrawElementsUShort"' in b.header:		
				values=ys.values(b.data,':')
				mode=values['"Mode"']			
				Size=None
				Offset=None
				Encoding=None
				ItemSize=None
				type=None
				if mode!='"LINES"':
					Indices=ys.get(b,'"Indices"')
					if Indices:
						values=ys.values(Indices[0].data,':')
						ItemSize=ys.getValue(values,'"ItemSize"','i')
						Uint16Array=ys.get(Indices[0],'"Uint16Array"')
						type="Uint16Array"
						print "DrawElementsUShort",type
						if Uint16Array:
							values=ys.values(Uint16Array[0].data,':')
							Size=ys.getValue(values,'"Size"','i')
							Offset=ys.getValue(values,'"Offset"','i')
							Encoding=ys.getValue(values,'"Encoding"','""')
							write(log,['Indice:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'magic:',magic],n)
							print Encoding
							if Encoding=='varint':
								path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
								if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
								if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
								if os.path.exists(path)==True:
									file=open(path,'rb')
									g=BinaryReader(file)
									magic,indiceList=getIndices(ItemSize,Size,Offset,type,g,mode,magic)
									indiceArray.append([indiceList,mode])
									file.close()
							else:
								path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
								if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
								if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
								if os.path.exists(path)==True:
									file=open(path,'rb')
									g=BinaryReader(file)
									g.seek(Offset)
									indiceList=g.H(ItemSize*Size)
									indiceArray.append([indiceList,mode])
									file.close()
				else:
					print 'LINES'
				
			if '"DrawElementsUByte"' in b.header:			
				values=ys.values(b.data,':')
				mode=values['"Mode"']			
				Size=None
				Offset=None
				Encoding=None
				ItemSize=None
				type=None
				if mode!='"LINES"':
					Indices=ys.get(b,'"Indices"')
					if Indices:
						values=ys.values(Indices[0].data,':')
						ItemSize=ys.getValue(values,'"ItemSize"','i')
						Uint8Array=ys.get(Indices[0],'"Uint8Array"')
						type="Uint8Array"
						print "DrawElementsUByte",type
						if Uint8Array:
							values=ys.values(Uint8Array[0].data,':')
							Size=ys.getValue(values,'"Size"','i')
							Offset=ys.getValue(values,'"Offset"','i')
							Encoding=ys.getValue(values,'"Encoding"','""')
							write(log,['Indice:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding,'magic:',magic],n)
							path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
							if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
							if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
							if os.path.exists(path)==True:
								file=open(path,'rb')
								g=BinaryReader(file)
								magic,indiceList=getIndices(ItemSize,Size,Offset,type,g,mode,magic)
								indiceArray.append([indiceList,mode])
								file.close()
				else:
					print 'LINES'
				
	return indiceArray
								
def getPath(File):
	path=os.path.dirname(input.filename)+os.sep+File.split('.gz')[0]
	if os.path.exists(path)==False:path=os.path.dirname(input.filename)+os.sep+File+'.txt'
	if os.path.exists(path)==False:path=os.path.dirname(input.filename)+os.sep+File
	if os.path.exists(path)==True:return path
	else:return None
			
def getVertexAttributeList(ys,VertexAttributeList,n):
	vertexArray=[]
	texArray=[]
	
	Vertex=ys.get(VertexAttributeList[0],'"Vertex"')			
	mode="Vertex"
	for b in Vertex:
		Size=None
		Offset=None
		Encoding=None
		ItemSize=None
		type=None				
		values=ys.values(b.data,':')
		if '"ItemSize"' in values:
			ItemSize=int(values['"ItemSize"'])					
			Int32Array=ys.get(b,'"Int32Array"')
			if Int32Array:
				type='Int32Array'
				print mode,type
				values=ys.values(Int32Array[0].data,':')
				Size=ys.getValue(values,'"Size"','i')
				Offset=ys.getValue(values,'"Offset"','i')
				File=ys.getValue(values,'"File"','""')
				Encoding=ys.getValue(values,'"Encoding"')
				write(log,['Vertex:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding],n)
				if Encoding=='"varint"':						
					path=getPath(File)
					if path:
						file=open(path,'rb')
						g=BinaryReader(file)
						bytes=decodeVarint(g,Offset,Size*ItemSize,type)
						vertexArray.append([bytes,Encoding,ItemSize])
						file.close()
						
			Float32Array=ys.get(b,'"Float32Array"')
			if Float32Array:
				type='Float32Array'
				print mode,type
				values=ys.values(Float32Array[0].data,':')
				Size=ys.getValue(values,'"Size"','i')
				Offset=ys.getValue(values,'"Offset"','i')
				File=ys.getValue(values,'"File"','""')
				Encoding=ys.getValue(values,'"Encoding"')
				write(log,['Vertex:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding],n)
				if Encoding!='"varint"':						
					path=getPath(File)
					if path:
						file=open(path,'rb')
						g=BinaryReader(file)
						g.seek(Offset)
						bytes=g.f(Size*ItemSize)
						list=[]
						for m in range(Size):
							list.append(bytes[m*ItemSize:m*ItemSize+ItemSize])
						vertexArray.append([list,Encoding])
						file.close()
							

			
	TexCoord0=ys.get(VertexAttributeList[0],'"TexCoord0"')
	if TexCoord0:
		mode="TexCoord0"
		for b in TexCoord0:
			Size=None
			Offset=None
			Encoding=None
			ItemSize=None
			type=None				
			values=ys.values(b.data,':')
			if '"ItemSize"' in values:
				ItemSize=int(values['"ItemSize"'])					
				Int32Array=ys.get(b,'"Int32Array"')
				if Int32Array:
					type='Int32Array'
					print mode,type
					values=ys.values(Int32Array[0].data,':')
					Size=ys.getValue(values,'"Size"','i')
					Offset=ys.getValue(values,'"Offset"','i')
					File=ys.getValue(values,'"File"','""')
					Encoding=ys.getValue(values,'"Encoding"')
					write(log,['TexCoord0:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding],n)
					if Encoding=='"varint"':						
						path=getPath(File)
						if path:
							file=open(path,'rb')
							g=BinaryReader(file)
							bytes=decodeVarint(g,Offset,Size*ItemSize,type)
							texArray.append([bytes,Encoding,ItemSize])
							file.close()
							
				Float32Array=ys.get(b,'"Float32Array"')
				if Float32Array:
					type='Float32Array'
					print mode,type
					values=ys.values(Float32Array[0].data,':')
					Size=ys.getValue(values,'"Size"','i')
					Offset=ys.getValue(values,'"Offset"','i')
					File=ys.getValue(values,'"File"','""')
					Encoding=ys.getValue(values,'"Encoding"')
					write(log,['TexCoord0:','mode:',mode,type,'Size:',Size,'Offset:',Offset,'Encoding:',Encoding],n)
					if Encoding!='"varint"':						
						path=getPath(File)
						if path:
							file=open(path,'rb')
							g=BinaryReader(file)
							g.seek(Offset)
							bytes=g.f(Size*ItemSize)
							list=[]
							for m in range(Size):
								u,v=bytes[m*ItemSize:m*ItemSize+ItemSize]
								list.append([u,1-v])
							texArray.append([list,Encoding])
							file.close()
									
	return	vertexArray,texArray							
			
def getRigGeometry(ys,parent,n):
	print '#'*50,'RigGeometry'
	n+=4
	BoneMap=[0]*1000
	bones=[]
	weights=[]
	mode=None
	indiceArray=[]
	vertexArray=[]
	texArray=[]
	atributes={}
	for child in parent.children:
		if "BoneMap" in child.header:
			write(log,['BoneMap'],n)
			values=ys.values(child.data,':')
			#print values
			for value in values:
				id=ys.getValue(values,value,'i')
				name=value.split('"')[1]
				BoneMap[id]=getSplitName(name,'_',-1)
		if "SourceGeometry" in child.header:
			values=ys.values(child.data,':')
			PrimitiveSetList=ys.get(child,'"PrimitiveSetList"')
			if PrimitiveSetList:
				indiceArray=getPrimitiveSetList(ys,PrimitiveSetList,n)
				
			UserDataContainer=ys.get(child,'"UserDataContainer"')
			if UserDataContainer:
				for UserData in UserDataContainer:
					Values=ys.get(UserData,'"Values"')
					if Values:
						for a in Values[0].children:
							values=ys.values(a.data,':')
							Name=ys.getValue(values,'"Name"','""')
							Value=ys.getValue(values,'"Value"','""')
							if Name:atributes[Name]=Value
						
			VertexAttributeList=ys.get(child,'"VertexAttributeList"')
			if VertexAttributeList:
				vertexArray,texArray=getVertexAttributeList(ys,VertexAttributeList,n)
			
				
		if "UserDataContainer" in child.header:
			write(log,['UserDataContainer'],n)
			Values=ys.get(child,'"Values"')
			if Values:
				for a in Values[0].children:
					values=ys.values(a.data,':')
					for value in values:
						id=ys.getValue(values,value)
						write(log,[value,':',id],n+4)
		if "VertexAttributeList" in child.header:
			write(log,['VertexAttributeList'],n)
			Bones=ys.get(child,'"Bones"')
			if Bones:
				write(log,['Bones'],n+4)
				values=ys.values(Bones[0].data,':')
				ItemSize=ys.getValue(values,'"ItemSize"','i')
				write(log,['"ItemSize"',':',ItemSize],n+8)
				Uint16Array=ys.get(Bones[0],'"Uint16Array"')
				if Uint16Array:
					type="Uint16Array"
					values=ys.values(Uint16Array[0].data,':')
					File=ys.getValue(values,'"File"','""')
					Size=ys.getValue(values,'"Size"','i')
					Offset=ys.getValue(values,'"Offset"','i')
					Encoding=ys.getValue(values,'"Encoding"','""')
					write(log,['"File"',':',File],n+8)
					write(log,['"Size"',':',Size],n+8)
					write(log,['"Offset"',':',Offset],n+8)
					write(log,['"Encoding"',':',Encoding],n+8)
					
					if Encoding=='varint':
						path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
						if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
						if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
						if os.path.exists(path)==True:
							file=open(path,'rb')
							g=BinaryReader(file)
							list=decodeVarint(g,Offset,Size*ItemSize,type)
							#write(log,list,0)
							for m in range(Size):
								bones.append(list[m*ItemSize:m*ItemSize+ItemSize])
							file.close()
					
					
			Weights=ys.get(child,'"Weights"')
			if Weights:
				write(log,['Weights'],n+4)
				values=ys.values(Weights[0].data,':')
				ItemSize=ys.getValue(values,'"ItemSize"','i')
				write(log,['"ItemSize"',':',ItemSize],n+8)
				Float32Array=ys.get(Weights[0],'"Float32Array"')
				if Float32Array:
					values=ys.values(Float32Array[0].data,':')
					File=ys.getValue(values,'"File"','""')
					Size=ys.getValue(values,'"Size"','i')
					Offset=ys.getValue(values,'"Offset"','i')
					Encoding=ys.getValue(values,'"Encoding"','""')
					write(log,['"File"',':',File],n+8)
					write(log,['"Size"',':',Size],n+8)
					write(log,['"Offset"',':',Offset],n+8)
					write(log,['"Encoding"',':',Encoding],n+8)
					
					if Encoding=='varint':
						path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
						if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
						if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
						if os.path.exists(path)==True:
							file=open(path,'rb')
							g=BinaryReader(file)
							list=decodeVarint(g,Offset,Size*ItemSize,type)
							#write(log,list,0)
							file.close()
					else:
						path=os.path.dirname(ys.filename)+os.sep+"model_file.bin.gz.txt"
						if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+"model_file.bin"
						if os.path.exists(path)==False:path=os.path.dirname(ys.filename)+os.sep+values['"File"'].split('"')[1]#+'.txt'
						if os.path.exists(path)==True:
							file=open(path,'rb')
							g=BinaryReader(file)
							g.seek(Offset)
							list=g.f(Size*ItemSize)
							#write(log,list,0)
							for m in range(Size):
								weights.append(list[m*ItemSize:m*ItemSize+ItemSize])
							file.close()
							
			
			
	#print atributes		
	mesh=Mesh()	
	if len(bones)>0 and len(Weights)>0:
		mesh.BoneMap=BoneMap
		skin=Skin()
		mesh.skinList.append(skin)
		mesh.skinIndiceList=bones
		mesh.skinWeightList=weights
	if len(indiceArray)>0:
		for [indices,mode] in indiceArray:
			print mode,len(indices)	
			mat=Mat()
			mesh.matList.append(mat)
			mat.IDStart=len(mesh.indiceList)
			mat.IDCount=len(indices)
			mesh.indiceList.extend(indices)
			if mode=='"TRIANGLE_STRIP"':mat.TRISTRIP=True
			if mode=='"TRIANGLES"':mat.TRIANGLE=True
			
		indices=indiceArray[0][0]
		mode=indiceArray[0][1]	
		if len(vertexArray)==1:
			if vertexArray[0][1]=='"varint"':
				bytes=vertexArray[0][0]				
				ItemSize=vertexArray[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(atributes['vtx_bbl_x'])
				s2=float(atributes['vtx_bbl_y'])
				s3=float(atributes['vtx_bbl_z'])
				s=[s1,s2,s3]			
				a1=float(atributes['vtx_h_x'])
				a2=float(atributes['vtx_h_y'])
				a3=float(atributes['vtx_h_z'])
				a=[a1,a2,a3]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				mesh.vertPosList=[floats[m:m+ItemSize]for m in range(0,len(floats),3)]
			else:
				list=vertexArray[0][0]
				mesh.vertPosList=list
				
		if len(texArray)==1:
			if texArray[0][1]=='"varint"':
				bytes=texArray[0][0]				
				ItemSize=texArray[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(atributes['uv_0_bbl_x'])
				s2=float(atributes['uv_0_bbl_y'])
				s=[s1,s2]			
				a1=float(atributes['uv_0_h_x'])
				a2=float(atributes['uv_0_h_y'])
				a=[a1,a2]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				#mesh.vertUVList=[floats[m:m+ItemSize]for m in range(0,len(floats),ItemSize)]
				for m in range(0,len(floats),ItemSize):
					u,v=floats[m:m+ItemSize]
					mesh.vertUVList.append([u,1-v])
			else:
				list=texArray[0][0]
				mesh.vertUVList=list
	return mesh	
	
				
	

def decodeQuantize(input,s,a,itemsize):
	x=[0]*len(input)
	id=0
	for r in range(len(input)/itemsize):
		for l in range(itemsize):
			x[id]=s[l]+input[id]*a[l]
			id+=1
	return x		
		
			
def getGeometry(ys,parent,n):
	print '#'*50,'Geometry'
	n+=4
	mode=None
	indiceArray=[]
	vertexArray=[]
	texArray=[]
	atributes={}
	
	write(log,['Geometry'],n)
	PrimitiveSetList=ys.get(parent,'"PrimitiveSetList"')
	if PrimitiveSetList:
		indiceArray=getPrimitiveSetList(ys,PrimitiveSetList,n)
		
	UserDataContainer=ys.get(parent,'"UserDataContainer"')
	if UserDataContainer:
		for UserData in UserDataContainer:
			Values=ys.get(UserData,'"Values"')
			if Values:
				for a in Values[0].children:
					values=ys.values(a.data,':')
					Name=ys.getValue(values,'"Name"','""')
					Value=ys.getValue(values,'"Value"','""')
					#if Name:write(log,[Name,Value],n+4)
					if Name:atributes[Name]=Value
				
	VertexAttributeList=ys.get(parent,'"VertexAttributeList"')
	if VertexAttributeList:
		vertexArray,texArray=getVertexAttributeList(ys,VertexAttributeList,n)
		
		
	#print atributes		
	mesh=Mesh()
	if len(indiceArray)>0:
		for [indices,mode] in indiceArray:
			print mode,len(indices)	
			mat=Mat()
			mesh.matList.append(mat)
			mat.IDStart=len(mesh.indiceList)
			mat.IDCount=len(indices)
			mesh.indiceList.extend(indices)
			if mode=='"TRIANGLE_STRIP"':mat.TRISTRIP=True
			if mode=='"TRIANGLES"':mat.TRIANGLE=True
			
		indices=indiceArray[0][0]
		mode=indiceArray[0][1]	
		if len(vertexArray)==1:
			if vertexArray[0][1]=='"varint"':
				bytes=vertexArray[0][0]				
				ItemSize=vertexArray[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(atributes['vtx_bbl_x'])
				s2=float(atributes['vtx_bbl_y'])
				s3=float(atributes['vtx_bbl_z'])
				s=[s1,s2,s3]			
				a1=float(atributes['vtx_h_x'])
				a2=float(atributes['vtx_h_y'])
				a3=float(atributes['vtx_h_z'])
				a=[a1,a2,a3]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				mesh.vertPosList=[floats[m:m+ItemSize]for m in range(0,len(floats),3)]
			else:
				list=vertexArray[0][0]
				mesh.vertPosList=list
				
		if len(texArray)==1:
			if texArray[0][1]=='"varint"':
				bytes=texArray[0][0]				
				ItemSize=texArray[0][2]
				if mode=='"TRIANGLE_STRIP"':
					bytes=decodePredict(indices,bytes,ItemSize)
				s1=float(atributes['uv_0_bbl_x'])
				s2=float(atributes['uv_0_bbl_y'])
				s=[s1,s2]			
				a1=float(atributes['uv_0_h_x'])
				a2=float(atributes['uv_0_h_y'])
				a=[a1,a2]
				floats=decodeQuantize(bytes,s,a,ItemSize)
				for m in range(0,len(floats),ItemSize):
					u,v=floats[m:m+ItemSize]
					mesh.vertUVList.append([u,1-v])
				
				
			else:
				list=texArray[0][0]
				mesh.vertUVList=list				
		
	return mesh	
	
	
	
	
def getMatrixTransform(ys,parent,n,boneParent):
	write(log,['MatrixTransform'],n)
	n+=4
	bone=Bone()	
	bone.name=str(len(skeleton.boneList))
	skeleton.boneList.append(bone)
	bone.parentName=boneParent.name
	
	
	Name=None
	for child in parent.children:
		values=ys.values(child.header,':')
		Name=ys.getValue(values,'"Name"','""')
		if Name:
			Name=getSplitName(Name,'_',-1)
			write(log,[Name],n)
			#if len(Name)<25:bone.name=Name
			boneIndeksList[Name]=bone.name
	
	
	for child in parent.children:
		if '"Matrix"' in child.header:
			floats=ys.values(child.data,'f')
			write(log,floats,n)
			bone.matrix=Matrix4x4(floats)
			bone.matrix*=boneParent.matrix
	for child in parent.children:
		if '"Children"' in child.header:
			getChildren(ys,child,n,bone)
		
	
def getSkeletonNode(ys,parent,n,boneParent):
	global firstmatrix
	write(log,['Skeleton'],n)
	n+=4
	bone=Bone()	
	bone.name=str(len(skeleton.boneList))
	skeleton.boneList.append(bone)
	bone.parentName=boneParent.name
	
	firstmatrix=boneParent.matrix
	
	Name=None
	for child in parent.children:
		values=ys.values(child.header,':')
		Name=ys.getValue(values,'"Name"','""')
		if Name:
			Name=getSplitName(Name,'_',-1)
			#print Name
			write(log,[Name],n)
			#if len(Name)<25:bone.name=Name
			boneIndeksList[Name]=bone.name
	
	
	for child in parent.children:
		if '"Matrix"' in child.header:
			floats=ys.values(child.data,'f')
			write(log,floats,n)
			bone.matrix=Matrix4x4(floats)
			bone.matrix*=boneParent.matrix
	for child in parent.children:
		if '"Children"' in child.header:
			getChildren(ys,child,n,bone)
	
def getRigGeometryNode(ys,parent,n,boneParent):	
	write(log,['RigGeometry'],n)			
	mesh=getRigGeometry(ys,parent,n)
	if len(mesh.vertPosList)>0:
		model.meshList.append(mesh)
		mesh.matrix=boneParent.matrix
						
	n+=4
	for child in parent.children:
		if '"Children"' in child.header:
			getChildren(ys,child,n,boneParent)
	
def getGeometryNode(ys,parent,n,boneParent):
	write(log,['Geometry'],n)
	mesh=getGeometry(ys,parent,n)
	if len(mesh.vertPosList)>0:
		model.meshList.append(mesh)
		mesh.matrix=boneParent.matrix


	n+=4
	for child in parent.children:
		if '"Children"' in child.header:
			getChildren(ys,child,n,boneParent)
	
def getBoneNode(ys,parent,n,boneParent):
	write(log,['Bone'],n)
	bone=Bone()
	bone.parentName=boneParent.name
	bone.name=str(len(skeleton.boneList))
	skeleton.boneList.append(bone)


	n+=4
	Name=None
	for child in parent.children:
		values=ys.values(child.header,':')
		#print child.header
		Name=ys.getValue(values,'"Name"','""')
		if Name:
			Name=getSplitName(Name,'_',-1)
			write(log,[Name],n)
			#print Name
			#if len(Name)<25:bone.name=Name
			boneIndeksList[Name]=bone.name
			
	for child in parent.children:
		if '"Matrix"' in child.header:
			values=ys.values(child.header,':')
			floats=ys.values(child.data,'f')
			bone.matrix=Matrix4x4(floats)
			bone.matrix*=boneParent.matrix
			
		if '"InvBindMatrixInSkeletonSpace"' in child.header:
			bindbone=Bone()
			#if Name:bindbone.name=Name
			bindbone.name=bone.name
			bindskeleton.boneList.append(bindbone)
			floats=ys.values(child.data,'f')
			write(log,[floats],n+4)
			matrix=Matrix4x4(floats).invert()
			bindbone.matrix=matrix*firstmatrix
			
	for child in parent.children:
		if '"Children"' in child.header:
			getChildren(ys,child,n,bone)
			
def getChildren(ys,parent,n,boneParent):
	write(log,['Children'],n)
	n+=4
	for child in parent.children:
		for a in child.children:
			if '"osg.MatrixTransform"' in a.header:
				getMatrixTransform(ys,a,n,boneParent)
			if '"osg.Node"' in a.header:
				getNode(ys,a,n,boneParent)
			if '"osgAnimation.Skeleton"' in a.header:
				getSkeletonNode(ys,a,n,boneParent)
			if '"osgAnimation.RigGeometry"' in a.header:
				getRigGeometryNode(ys,a,n,boneParent)
			if '"osg.Geometry"' in a.header:
				getGeometryNode(ys,a,n,boneParent)
			if '"osgAnimation.Bone"' in a.header:
				getBoneNode(ys,a,n,boneParent)
		
	
def getNode(ys,parent,n,boneParent):
	write(log,['Node'],n)
	n+=4
	
	
	bone=Bone()	
	bone.name=str(len(skeleton.boneList))
	skeleton.boneList.append(bone)
	bone.parentName=boneParent.name
	bone.matrix=boneParent.matrix
	
	Name=None
	for child in parent.children:
		values=ys.values(child.header,':')
		Name=ys.getValue(values,'"Name"','""')
		if Name:
			#Name=getSplitName(Name,'_',-1)
			write(log,[Name],n)
			#if len(Name)<25:bone.name=Name
			boneIndeksList[Name]=bone.name
	
	for child in parent.children:
		if '"Children"' in child.header:
			getChildren(ys,child,n,bone)
	
	
				
def bindPose(bindSkeleton,poseSkeleton,meshObject):
		#print 'BINDPOSE'
		mesh=meshObject.getData(mesh=1)		
		poseBones=poseSkeleton.getData().bones
		bindBones=bindSkeleton.getData().bones	
		#mesh.transform(meshObject.matrixWorld)	
		mesh.update()
		for vert in mesh.verts:
			index=vert.index
			skinList=mesh.getVertexInfluences(index)
			vco=vert.co.copy()*meshObject.matrixWorld
			vector=Vector()
			sum=0
			for skin in skinList:
				bone=skin[0]							
				weight=skin[1]	
				if bone in bindBones.keys() and bone in poseBones.keys():	
					matA=bindBones[bone].matrix['ARMATURESPACE']*bindSkeleton.matrixWorld
					matB=poseBones[bone].matrix['ARMATURESPACE']*poseSkeleton.matrixWorld
					vector+=vco*matA.invert()*matB*weight
					sum+=weight
				else:
					vector=vco
					break
			vert.co=vector
		mesh.update()
		Blender.Window.RedrawAll()	
	
	
def osgParser(filename):
	global skeleton,bindskeleton,model,boneIndeksList,firstmatrix
	boneIndeksList={}
	model=Model(filename)
	skeleton=Skeleton()
	skeleton.ARMATURESPACE=True
	bindskeleton=Skeleton()
	bindskeleton.NICE=True
	bindskeleton.ARMATURESPACE=True
	ys=Yson()
	ys.log=True
	ys.filename=filename
	ys.parse()
	
	firstmatrix=Matrix4x4([1,0,0,0,0,0,1,0,0,-1,0,0,0,0,0,1])
	
	n=0
	bone=Bone()
	bone.matrix=Matrix().resize4x4()
	bone.name=str(len(skeleton.boneList))
	bone.name='scene'
	skeleton.boneList.append(bone)
	Node=ys.get(ys.root,'"osg.Node"')
	if Node:
		getNode(ys,Node[0],n,bone)
	if len(bindskeleton.boneList)>0:bindskeleton.draw()	
	
	for mesh in model.meshList:
		if len(mesh.skinList)>0:
			for map in mesh.BoneMap:
				if map==0:break
				mesh.boneNameList.append(boneIndeksList[map])
	
	
	for mesh in model.meshList:
			if len(mesh.skinList)>0:
				skeleton.NICE=True
				skeleton.draw()			
				break
				
						
	
	for mesh in model.meshList:
		mesh.draw()
		if mesh.object:
			if len(mesh.skinList)>0:
				if BINDPOSE==1:
					if bindskeleton.object and skeleton.object:
						mesh.object.getData(mesh=1).transform(mesh.matrix)
						mesh.object.getData(mesh=1).update()
						##mesh.object.setMatrix(mesh.matrix)
						bindPose(bindskeleton.object,skeleton.object,mesh.object)
						##mesh.object.setMatrix(mesh.matrix.invert()*mesh.object.matrixWorld)
						scene = bpy.data.scenes.active
						scene.objects.unlink(bindskeleton.object)
				else:
					if bindskeleton.object and skeleton.object:
						mesh.object.getData(mesh=1).transform(mesh.matrix)
						mesh.object.getData(mesh=1).update()
					
					
			else:		
				mesh.object.setMatrix(mesh.matrix)
		
	n=0	
	Animations=ys.get(ys.root,'"osgAnimation.Animationnnnn"')		
	if Animations:
		for animation in Animations:	
			getAnimation(ys,animation,n)

def Parser():
	global log
	log=open('log.txt','w')
	filename=input.filename
	ext=filename.split('.')[-1].lower()
	osgParser(filename)	
	log.close()
	# ------------------------------- Ylvgn
	global build_args
	model_path = build_args["model_path"]
	build_path = build_args["build_path"]
	output_path = os.path.join(build_path, "decode.blend")
	rm_list = [
		os.path.join(model_path, "log.txt"),
		os.path.join(model_path, "file.osgjs.ys"),
	]
	for file_path in rm_list:
		if os.path.exists(file_path):
			os.remove(file_path)
	Blender.Save(output_path, 1)

def openFile(flagList): 
	global input, output
	input=Input(flagList)
	output=Output(flagList)
	parser=Parser()

# Please use CLI: blender.exe -b -P decode_osgjs.py --model_path <osgjs_dir_path>
if __name__ == '__main__':
	global build_args
	arg_config = {
		"model_path" : str, # file.osgjs所在的文件夹目录路径
		"build_path" : str, # 生成.blend的目录路径, 无传则认为在model_path中生成.blend
	}
	build_args = build_args_parser.parse(arg_config)
	if build_args.get("model_path", None):
		model_path = build_args["model_path"]
		files = os.listdir(model_path)
		osgjs_fn = ""
		for file in files:
			if file.endswith(".osgjs"):
				osgjs_fn = file
				break
		if osgjs_fn:
			osgjs_path = os.path.join(model_path, osgjs_fn)
			if not (build_args.get("build_path", None)):
				build_args["build_path"] = model_path
			openFile(osgjs_path)
		else:
			print(".osgjs file not exists dir_path=%s" % model_path)
			sys.exit(1)
	else:
		print("not send params '--model_path' ")
		sys.exit(1)
	