#!BPY

"""
Name: 'COLLADA 1.3.1 (.dae) ...'
Blender: 237
Group: 'Import'
Tooltip: 'Import scene from COLLADA format (.dae)'
"""

__author__ = "Mikael Lagre"
__url__ = ("blender", "blenderartist.org", "Project homepage, http://colladablender.sourceforge.net",)
__version__ = "0.4"
__bpydoc__ = """\Description: Imports a COLLADA 1.3.1 file into a Blender scene.
Usage: Run the script from the menu or inside Blender.  
Notes: Does not import animation.
"""

# --------------------------------------------------------------------------
# Collada importer version 0.2
# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2005: Mikael Lagre' contactme@mikaellagre.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------


_ERROR = False



try:
    import math
except:
    print "Error! Could not find math module"
    _ERROR = True

try:
    import Blender
    from Blender import *
except:
    print "Error! Could not find Blender modules!"
    _ERROR = True


try:
    from xml.dom.minidom import *
except:
    print 'Error! Could not find reader.Sax2 module'
    _ERROR = True

if _ERROR:
	from sys import version_info
	version = '%s.%s' % version_info[0:2]
	print """
This script requires the xml module that is part of a
default standalone Python install.

To run the collada importer and exporter you need to have
Python version %s installed in your system. It can be downloaded from:

http://www.python.org

Notes:
- The minor (third) version number doesn't matter, you can have either
Python %s.1 or %s.2 or higher.
- If you do have Python %s installed and still can't run the scripts, then
make sure Blender's Python interpreter is finding the standalone modules
(run 'System Information' from Blender's Help -> System menu).
""" % (version, version, version, version)
	Draw.PupMenu("Please install full version of python %t | Check the console for more info")
	
import re

#filename = 'C:\\test.xml'
whitespace = re.compile( '\s+' )
angleToRadian = 3.1415926 / 180.0
radianToAngle = 180.0 / 3.1415926
warnings = False

class Param:
    name = None
    type = None
    flow = None
    data = None
    
    def __init__( self, elementNode ):
        self.name = CP.PN.toConstant( CP.PN(), elementNode.attributes.getNamedItem( 'name' ).value )
        self.type = elementNode.attributes.getNamedItem( 'type' )
        if ( self.type != None ):
            self.type = self.type.value
        self.flow = elementNode.attributes.getNamedItem( 'flow' )
        if ( self.flow != None ):
            self.flow = self.flow.value
        firstChild = elementNode.firstChild
        if ( firstChild is not None ):
            if ( firstChild.nodeType == Node.TEXT_NODE ):
                self.data = firstChild.nodeValue
        
class Technique:
    profile = None
    def __init__( self, elementNode ):
        self.profile = CP.toConstantProfile( CP(), elementNode.attributes.getNamedItem( 'profile' ).value )

class Input:
    idx = None
    semantic = None
    source = None
    def __init__( self, elementNode ):
        self.idx = elementNode.attributes.getNamedItem( 'idx' )
        if ( self.idx is not None ):
            self.idx = self.idx.value
        self.semantic = CP.IS.toConstant( CP.IS(), elementNode.attributes.getNamedItem( 'semantic' ).value )
        self.source = elementNode.attributes.getNamedItem( 'source' ).value  

class Source:
    
    #id = None
    #name = None
    #data = None
    #count = None
    #params = None
    
    def __init__( self, sourceNode ):
        
        self.id = sourceNode.attributes.getNamedItem( 'id' ).value
        # self.name = sourceNode.attributes.getNamedItem( 'name' ).value
        self.data = []
        self.params = 0
        self.count = None
        
        # Get COMMON profile
        techniqueElements = sourceNode.getElementsByTagName( 'technique' )
        commonProfile = getCommonProfile( techniqueElements )
        if not ( commonProfile is None ):
            accessorElements = commonProfile.getElementsByTagName( 'accessor' )
            
            # Get first accessor only
            if ( accessorElements ):
                accessor = accessorElements[ 0 ]
                source = accessor.attributes.getNamedItem( 'source' ).value
                source = source[1:]
                count = accessor.attributes.getNamedItem( 'count' ).value
                
                # Get nr Params in order to store list in our data list
                paramElements = accessor.getElementsByTagName( 'param' )
                
                # NOTE: For this routine it does not matter what the param
                # values are since they are accessed logically when reading
                # the face values
                nrParams = len( paramElements )
                
                # Get source array
                float_arrays = sourceNode.getElementsByTagName( 'float_array' )
                
                for array in float_arrays:
                    id = array.attributes.getNamedItem( 'id' ).value
                    if ( id == source ):
                        rawData = getRawData( array )
                        if ( nrParams == 1 ):
                            for index in range( 0, len( rawData ), nrParams ):
                                self.data.append( float( rawData[ index ] ) )
                        elif ( nrParams == 2 ):
                            for index in range( 0, len( rawData ), nrParams ):
                                data = float( rawData[ index ] ), float( rawData[ index + 1 ] ) 
                                self.data.append( data )
                        elif ( nrParams == 3 ):
                            for index in range( 0, len( rawData ), nrParams ):
                                data = float( rawData[ index ] ), float( rawData[ index + 1 ] ), float( rawData[ index + 2 ] )
                                self.data.append( data )

    
def getParamData( elementNode ):
    return Param( elementNode )

def getTechniqueData( elementNode ):
    return Technique( elementNode )

def getInputData( elementNode ):
    return Input( elementNode )

def getCommonProfile( techniqueElements ):
    for technique in techniqueElements:
        techniqueData = Technique( technique )
        if ( techniqueData.profile == CP.COMMON ):
            return technique
    return None

def toFloat3( stringValue ):
    split = stringValue.split( )  #whitespace.split( stringValue, 2 )
    return [ float( split[ 0 ] ), float( split[ 1 ] ), float( split[ 2 ] ) ]

def toMatrix4x4( matrixElement ):
    m = getRawData( matrixElement )
    
    vec1 = [ float(m[0]), float(m[4]), float(m[8]), float(m[12]) ]
    vec2 = [ float(m[1]), float(m[5]), float(m[9]), float(m[13]) ]
    vec3 = [ float(m[2]), float(m[6]), float(m[10]), float(m[14]) ]
    vec4 = [ float(m[3]), float(m[7]), float(m[11]), float(m[15]) ]
    
    return Mathutils.Matrix( vec1, vec2, vec3, vec4 )

def getRawData( arrayElement ):
    firstChild = arrayElement.firstChild
    if ( firstChild is not None ):
        if ( firstChild.nodeType == Node.TEXT_NODE ):
            data = firstChild.nodeValue.split( )
            return data
    
    # Find correct element

def getElements( myNode, tagName ):
    nodes = []
    for child in myNode.childNodes:
        if child.nodeName == tagName:
            nodes.append( child )
    
    return nodes

# Make a Euler object with radian angles instead
def toEulerAngleInRadians( euler ):
    euler.x *= angleToRadian
    euler.y *= angleToRadian
    euler.z *= angleToRadian
    return euler

def addVec3( vector1, vector2 ):
    vector1.x += vector2.x
    vector1.y += vector2.y
    vector1.z += vector2.z

def getEuler( rotateElement ):
    data = getRawData( rotateElement )
    euler = [ float( data[ 0 ] ) * float( data[ 3 ] ) * angleToRadian,
              float( data[ 1 ] ) * float( data[ 3 ] ) * angleToRadian,
              float( data[ 2 ] ) * float( data[ 3 ] ) * angleToRadian ]
    return Mathutils.Euler( euler )

def getVector3( element ):
    data = getRawData( element )
    value = [ float( data[ 0 ] ), float( data[ 1 ] ), float( data[ 2 ] ) ]
    return Mathutils.Vector( value )

def getImageSourcePath( source, filePath ):
    
    # Try and load our texture from 'filePath' (local .dae import path)
    texturesDir = filePath + '/'
    texturesDir = texturesDir.replace( '\\', '/' )  # Bill Gates!!!
    splitPath = source.split( '/' )
    if ( len( splitPath ) > 0 ):
        fileName = splitPath[ len( splitPath ) - 1 ]
        mupp = texturesDir + fileName
        if ( Blender.sys.exists( mupp ) == 1 ):
            return mupp
    
    # File does not exist to try and remove characters from string and see if file exists
    source = source.replace( 'file://', '' )
    if ( Blender.sys.exists( source ) == 1 ):
        return source
        
    source = source.replace( 'file://.', '' )
    if ( Blender.sys.exists( source ) == 1 ):
        return source
    
        
    # File did not exists so try and load our texture from 'texturesdir'
    texturesDir = Blender.Get( 'texturesdir' )
    texturesDir = texturesDir.replace( '\\', '/' ) # Bill Gates!!!
    splitPath = source.split( '/' )
    if ( len( splitPath ) > 0 ):
        fileName = splitPath[ len( splitPath ) - 1 ]
        source = texturesDir + fileName
        if ( Blender.sys.exists( source ) == 1 ):
            return source
    
    return None

# COLLADA Common Profile constants strings
# ( for COLLADA specification 1.3.1 )
# Also in this collada common profile class is library type constants
# flow types and other xs:NMTOKEN constants definied in the schema
class _CommonProfile:
    
    COMMON = 1
    BLENDER = 2
    
    str = [ "", "COMMON", "BLENDER" ]
    
    def toConstantProfile( self, str ):
        index = 0
        for s in _CommonProfile.str:
            if ( s == str ):
                return index
            index += 1     
    
    class _ParamName:
        A = 1
        AMBIENT = 2
        ANGLE = 3
        ATTENUATION = 4
        ATTENUATION_SCALE = 5
        B = 6
        BOTTOM = 7
        COLOR = 8
        DIFFUSE = 9
        EMISSION = 10
        FALLOFF = 11
        FALLOFF_SCALE = 12
        G = 13
        LEFT = 14
        P = 15
        Q = 16
        R = 17
        REFLECTIVE = 18
        REFLECTIVITY = 19
        RIGHT = 20
        S = 21
        SHININESS = 22
        SPECULAR = 23
        T = 24
        TANGENT_X = 25
        TANGENT_Y = 26
        TANGENT_Z = 27
        TIME = 28
        TOP = 29
        TRANSPARENCY = 30
        TRANSPARENT = 31
        U = 32
        V = 33
        W = 34
        X = 35
        XFOV = 36
        Y = 37
        YFOV = 38
        Z = 39
        ZFAR = 40
        ZNEAR = 41
        
        str = [ "", "A", "AMBIENT", "ANGLE", "ATTENUATION", 
                "ATTENUATION_SCALE", "B", "BOTTOM", "COLOR", "DIFFUSE",
                "EMISSION", "FALLOFF", "FALLOFF_SCALE", "G", "LEFT",
                "P", "Q", "R", "REFLECTIVE", "REFLECTIVITY", "RIGHT", "S", 
                "SHININESS", "SPECULAR", "T", "TANGENT.X", "TANGENT.Y", 
                "TANGENT.Z", "TIME", "TOP", "TRANSPARENCY", "TRANSPARENT",
                "U", "V", "W", "X", "XFOV", "Y", "YFOV", "Z", "ZFAR", "ZNEAR" ]
    
        def toConstant( self, str ):
            index = 0
            for s in CP.PN.str:
                if ( s == str ):
                    return index
                index += 1     
    
    class _ProgramIDAndURL:
        ANGLE_MAP = 1
        BEZIER = 2
        BSPLINE = 3
        CARDINAL = 4
        CONSTANT = 5
        CUBE_MAP = 6
        FISH_EYE = 7
        HERMITE = 8
        LAMBERT = 9
        LINEAR = 10
        ORTHOGRAPHIC = 11
        PANORAMA = 12
        PERSPECTIVE = 13
        PHONG = 14
        REAR_FISH_EYE = 15
        SPHERICAL = 16
        
        str = [ "", "ANGLE_MAP", "BEZIER", "BSPLINE", "CARDINAL", "CONSTANT",
                "CUBE_MAP", "FISH_EYE", "HERMITE", "LAMBERT", "LINEAR",
                "ORTHOGRAPHIC", "PANORAMA", "PERSPECTIVE", "PHONG",
                "REAR_FISH_EYE", "SPHERICAL" ]

        def toConstant( self, str ):
            index = 0
            for s in CP.PIAU.str:
                if ( s == str ):
                    return index
                index += 1 

    class _CodeAndEntrySemantic:
        FRAGMENT_PROGRAM = 1
        VERTEX_PROGRAM = 2
    
    class _InputSemantic:
        BIND_SHAPE_NORMAL = 1
        BIND_SHAPE_POSITION = 2
        BINORMAL = 3
        COLOR = 4
        IMAGE = 5
        INPUT = 6
        IN_TANGENT = 7
        INTERPOLATION = 8
        INV_BIND_MATRIX = 9
        JOINT = 10
        JOINTS_AND_WEIGHTS = 11
        NORMAL = 12
        OUTPUT = 13
        OUT_TANGENT = 14
        POSITION = 15
        TANGENT = 16
        TEXCOORD = 17
        TEXTURE = 18
        UV = 19
        VERTEX = 20
        WEIGHT = 21
        
        str = [ "", "BIND_SHAPE_NORMAL", "BIND_SHAPE_POSITION", "BINORMAL",
                "COLOR", "IMAGE", "INPUT", "IN_TANGENT", "INETRPOLATION", 
                "INV_BIND_MATRIX", "JOINT", "JOINTS_AND_WEIGHTS", "NORMAL",
                "OUTPUT", "OUT_TANGENT", "POSITION", "TANGENT", "TEXCOORD",
                "TEXTURE", "UV", "VERTEX", "WEIGHT" ]
    
        def toConstant( self, str ):
            index = 0
            for s in CP.IS.str:
                if ( s == str ):
                    return index
                index += 1    
    
    class _ChannelAndControllerTarget:
        #( # )[( # )]
        A = 1
        ANGLE = 2
        B = 3
        G = 4
        P = 5
        Q = 6
        R = 7
        S = 8
        T = 9
        TIME = 10
        U = 11
        V = 12
        W = 13
        X = 14
        Y = 15
        Z = 16
    
    class _LibraryType:
        ANIMATION = 1
        CAMERA = 2
        CODE = 3
        CONTROLLER = 4
        GEOMETRY = 5
        IMAGE = 6
        LIGHT = 7
        MATERIAL = 8
        PROGRAM = 9
        TEXTURE = 10
        
        str = [ "", "ANIMATION", "CAMERA", "CODE", "CONTROLLER", "GEOMETRY",
                "IMAGE", "LIGHT", "MATERIAL", "PROGRAM", "TEXTURE" ]
    
        def toConstant( self, str ):
            index = 0
            for s in CP.LT.str:
                if ( s == str ):
                    return index
                index += 1
    
    class _FlowType:
        IN = 1
        OUT = 2
        INOUT = 3
        
        str = [ "", "IN", "OUT", "INOUT" ]
        
        def toConstant( self, str ):
            index = 0
            for s in CP.FT.str:
                if ( s == str ):
                    return index
                index += 1
    
    class _NodeType:
        NODE = 1
        JOINT = 2
        
        str = [ "", "NODE", "JOINT" ]

        def toConstant( self, str ):
            index = 0
            for s in CP.NT.str:
                if ( s == str ):
                    return index
                index += 1
                
    
    class _LightType:
        AMBIENT = 1
        DIRECTIONAL = 2
        POINT = 3
        SPOT = 4
        
        str = [ "", "AMBIENT", "DIRECTIONAL", "POINT", "SPOT" ]
        
        def toConstant( self, str ):
            index = 0
            for s in CP.LIGHT.str:
                if ( s == str ):
                    return index
                index += 1

    # Definition of modules for easier access in code
    # Note: This is pretty stupid I know ...
    
    class PN( _ParamName ):
        pass
    class PIAU( _ProgramIDAndURL ):
        pass
    class CAES( _CodeAndEntrySemantic ):
        pass
    class IS( _InputSemantic ):
        pass
    class CACT( _ChannelAndControllerTarget ):
        pass
    class LT( _LibraryType ):
        pass
    class FT( _FlowType ):
        pass
    class NT( _NodeType ):
        pass
    class LIGHT( _LightType ):
        pass

# Common Profile
class CP( _CommonProfile ):
    pass


def importImage( imageElement, filePath ):
    
    global library
    global warnings
    
    # Get attributes
    source = imageElement.attributes.getNamedItem( 'source' )
    id = imageElement.attributes.getNamedItem( 'id' ).value
    name = imageElement.attributes.getNamedItem( 'name' )

    
    # Get a correct source
    imageSource = None
    if ( source != None ):
        source = source.value
        imageSource = getImageSourcePath( source, filePath )
    
    blenderImage = None
    if not ( imageSource == None ): 
        blenderImage = Image.Load( imageSource )
        if ( name != None ):
            blenderImage.setName( name.value )
        elif ( id != None ):
            blenderImage.setName( id )
    else:
        print 'Warning: Texture %s could not be loaded. Check if texture exist or modify texture path in .dae file' % ( source )
        warnings = True
    
    return id, blenderImage
    
def importTexture( textureElement ):
    
    global library
    
    # Get <texture> attributes
    id = textureElement.attributes.getNamedItem( 'id' ).value
    name = textureElement.attributes.getNamedItem( 'name' )
    if name != None:
        name = name.value
    else:
        name = id
    
    # Create new texture
    blenderTexture = Texture.New( name )
    
    # Check for supported texture param
    # Current support is only DIFFUSE
    params = textureElement.getElementsByTagName( 'param' )
    imageType = 'Image'
    for param in params:
        paramData = getParamData( param )
        if ( paramData.name == CP.PN.DIFFUSE ):
            imageType = 'Image'
            break;
    
    # Set texture type
    blenderTexture.setType( imageType )
    
    # Get common profile
    techniques = textureElement.getElementsByTagName( 'technique' )
    commonProfile = getCommonProfile( techniques )
    
    if ( commonProfile is not None ):
        inputs = commonProfile.getElementsByTagName( 'input' )
        for input in inputs:
            inputData = getInputData( input )
            if ( inputData.semantic == CP.IS.IMAGE ):
                source = inputData.source
                source = source.replace( '#', '' )
                if ( library.has_key( source ) ):
                    imageSource = library[ source ]
                    if ( imageSource != None ):
                        blenderTexture.setImage( imageSource )
    
    return id, blenderTexture
    
def importMaterial( materialElement ):

    global library
    
    id = materialElement.attributes.getNamedItem( 'id' ).value
    name = materialElement.attributes.getNamedItem( 'name' )
    if name != None:
        name = name.value
    else:
        name = id
    material = Material.New( name )
    
    # Get shader(s)
    shaders = materialElement.getElementsByTagName( 'shader' )
    shader = None
    if ( len( shaders ) > 1 ):
        print 'Warning: Multiple shaders on material %s' % id
        print 'First shader data used only'
    
    shader = shaders[ 0 ]
   

    # Get COMMON technique
    techniques = shader.getElementsByTagName( 'technique' )
    common = getCommonProfile( techniques )
    
    if ( common ):
        
        # TODO: Create a LAMBERT diffuse shader and PHONG specular shader
        # NOTE: This is not supported yet in Blender 2.37
        
        # Get first pass only
        passes = common.getElementsByTagName( 'pass' )
        firstPass = None
        if ( len( passes ) > 1 ):
            print 'Warning shader has multiple passes. Using first pass only'
        
        firstPass = passes[ 0 ]
       

        # Get input semantics
        inputSemantics = firstPass.getElementsByTagName( 'input' )
        textureSlot = 0
        for input in inputSemantics:
            if ( textureSlot < 9 ):
                inputData = getInputData( input )
                
                # Check for TEXTURE semantic. If present create link to texture
                if ( inputData.semantic == CP.IS.TEXTURE ):
                    source = inputData.source.replace( '#', '' )
                    # texture = Texture.Get( source )
                    texture = library[ source ]
                    if ( texture != None ):
                        
                        # Default: Map to color and use UV as tex coordinates.
                        material.setTexture( textureSlot, texture, Texture.TexCo.UV, Texture.MapTo.COL )
                        
                        # Increase texture slot
                        textureSlot += 1
            else:
                print 'Warning: More than 8 textures linked to this material. Additional texture(s) ignored'
                break;

        
        # Get program (if any)
        programs = shader.getElementsByTagName( 'program' )
        
        if ( programs is not None ):
            program = programs[ 0 ]
            
            # Evaluate params
            transparent = 1.0, 1.0, 1.0
            transparency = 1.0
            params = program.getElementsByTagName( 'param' )
            for param in params:
                paramData = getParamData( param )
                name = paramData.name
                if ( name == CP.PN.COLOR ):
                    material.setRGBCol( toFloat3( paramData.data ) )
                elif ( name == CP.PN.DIFFUSE ):
                    material.setRGBCol( toFloat3( paramData.data ) )
                elif ( name == CP.PN.AMBIENT ):
                    ambient = Mathutils.Vector( toFloat3( paramData.data ) )
                    material.setAmb( ambient.length )
                elif ( name == CP.PN.SPECULAR ):
                    material.setSpecCol( toFloat3( paramData.data ) )
                elif ( name == CP.PN.EMISSION ):
                    emission = Mathutils.Vector( toFloat3( paramData.data ) )
                    material.setEmit( emission.length )
                elif ( name == CP.PN.SHININESS ):
                    shininess = float( paramData.data) * 4.0
                    material.setHardness( int( shininess ) )
                elif ( name == CP.PN.TRANSPARENT ):
                    transparent = Mathutils.Vector( toFloat3( paramData.data) )
                    material.setAlpha( 1.0 - transparent.length )
                elif ( name == CP.PN.TRANSPARENCY ):
                    transparent *= float( paramData.data )
                    material.setAlpha( 1.0 - transparent.length )
                elif ( name == CP.PN.REFLECTIVE ):
                    material.setMirCol( toFloat3( paramData.data ) )
                elif ( name == CP.PN.REFLECTIVITY ):
                    reflectivity = float( paramData.data )
                    material.setRef( reflectivity )
    
    return id, material

def importGeometry( geometryElement ):
    
    global library
    
    id = geometryElement.attributes.getNamedItem( 'id' ).value    
    name = geometryElement.attributes.getNamedItem( 'name' )
    
    
    # Get mesh element
    meshes = geometryElement.getElementsByTagName( 'mesh' )
    if not ( meshes == None ):
        mesh = meshes[ 0 ]
        
        # Set name
        if name:
            name = name.value
        else:
            name = id
        
        # Create mesh
        nmesh = Blender.NMesh.New( name )
                
        # Get sources
        sourceList = dict()
        sourceElements = mesh.getElementsByTagName( 'source' )
        for sourceElement in sourceElements:
            source = Source( sourceElement )
            sourceList[ source.id ] = source
        
        
        # Get vertices element
        
        vPos = None
        vNormal = None
        vTexCoord = None        
        
        verticesElements = mesh.getElementsByTagName( 'vertices' )
        if not ( verticesElements is None ):
            vertices = verticesElements[ 0 ]
            
            # Get input semantics for this element
            inputs = vertices.getElementsByTagName( 'input' )
            for input in inputs:
                inputData = getInputData( input )
                if ( inputData.semantic == CP.IS.POSITION ):
                    vPos = sourceList[ inputData.source[1:] ]
                elif ( inputData.semantic == CP.IS.NORMAL ):
                    vNormal = sourceList[ inputData.source[1:] ]
                elif ( inputData.semantic == CP.IS.TEXCOORD ):
                    vTexCoord = sourceList[ inputData.source[1:] ]
                    nmesh.hasVertexUV( 1 )
        
        # Get <polygons>, <triangles> element
        polygonElements = mesh.getElementsByTagName( 'polygons' )
        if ( polygonElements == None ):
            polygonElements = mesh.getElementsByTagName( 'triangles' )
        if ( polygonElements == None ):
            print 'Unsupported mesh data type import!'
        
        for polygons in polygonElements:
            
            # Mesh information lists
            pVertices = []            
            pNormal = None
            pTexCoord = None
            
            # Get material and create new Material if we could not find any
            material = None
            materialSource = polygons.attributes.getNamedItem( 'material' )
            if ( materialSource != None ):
                materialSource = materialSource.value
                materialSource = materialSource[1:]
                if ( materialSource != '' ):
                    material = library[ materialSource ]
                    # material = Material.Get( materialSource ) 

            
            # Add material to mesh (if present)
            firstImage = None
            if ( material != None ):
                nmesh.addMaterial( material )
                
                # Get first image of first texture and set it to each face
                textures = material.getTextures()
                firstImage = None
                if len( textures ) > 0:
                    firstTexture = textures[ 0 ]
                    if ( firstTexture != None ):
                        firstImage = firstTexture.tex.image
            
            
            # Get input semantics
            inputElements = polygons.getElementsByTagName( 'input' )
            inputSemantics = []
            nrSemantics = 0
            for input in inputElements:
                inputData = getInputData( input )
                inputSemantics.append( inputData.semantic )
                nrSemantics += 1
                if ( inputData.semantic == CP.IS.VERTEX ):
                    
                    # Create NMesh vertices list
                    vIndex = 0
                    for v in vPos.data:
                        vertex = NMesh.Vert( v[ 0 ], v[ 1 ], v[ 2 ] )
                        vertex.index = vIndex
##                        if not ( vNormal is None ):
##                            vertex.normal = Mathutils.Vector( vNormal.data[ vIndex ] )
                        if not ( vTexCoord is None ):
                            vertex.uvco = Mathutils.Vector( vTexCoord.data[ vIndex ] )
                        pVertices.append( vertex )
                        vIndex += 1
                    
                    # Set NMesh vertices list
                    nmesh.verts = pVertices
                    
                elif ( inputData.semantic == CP.IS.NORMAL ):
                    pNormal = sourceList[ inputData.source[1:] ]
                elif ( inputData.semantic == CP.IS.TEXCOORD ):
                    nmesh.hasFaceUV( 1 )
                    pTexCoord = sourceList[ inputData.source[1:] ]                    


            # Create Face for each p element
            pElements = polygons.getElementsByTagName( 'p' )
            for p in pElements:
                polygonData = getRawData( p )                
                nrVertices = len( polygonData ) / nrSemantics
                newFace = NMesh.Face( )
                vIndex = 0
                for s in range( nrVertices ):
                    semanticIndex = 0
                    vList = []
                    nList = []
                    perFaceUV = []
                    
                    for semantic in inputSemantics:
                        arrIndex = vIndex * nrSemantics + semanticIndex
                        index = int( polygonData[ arrIndex ] )
                        vert = None
                        if ( semantic == CP.IS.VERTEX ):
                            vert = pVertices[ index ]
                            # vList.append( vert )
                            newFace.append( vert )
                        elif ( semantic == CP.IS.NORMAL ):
                            if not ( vert is None ):
                                vert.no = pNormal.data[ index ]
                        elif ( semantic == CP.IS.TEXCOORD ):
                            #perFaceUV.append( pTexCoord.data[ index ] )
                            newFace.uv.append( pTexCoord.data[ index ] )
                        
                        semanticIndex +=1
                    vIndex += 1
                    
                # newFace.uv = perFaceUV
                if ( firstImage != None ):
                    newFace.image = firstImage
                newFace.mode |= Blender.NMesh.FaceModes[ 'TEX' ]
                if ( material != None ):
                    newFace.materialIndex = 0
                newFace.hide = 0
                newFace.smooth = 0
                nmesh.addFace( newFace )
            
            # Put mesh in blender
            nmesh.update( 1, 0, 0 )
            
            
            return id, nmesh
    
def importLight( lightElement ):
    
    # Get light type and id
    name = lightElement.attributes.getNamedItem( 'name' )
    id = lightElement.attributes.getNamedItem( 'id' ).value
    type = lightElement.attributes.getNamedItem( 'type' )
    newLight = None
    if type != None:
        type = type.value
        if ( type == 'AMBIENT' ):
            newLight = Lamp.New( 'Hemi' )
        elif ( type == 'DIRECTIONAL' ):
            newLight = Lamp.New( 'Sun' )
        elif ( type == 'SPOT' ):
            newLight = Lamp.New( 'Spot' )
        elif ( type == 'POINT' ):
            newLight = Lamp.New( 'Lamp' )
    else:
        type = 'POINT'
        newLight = Lamp.New( 'Lamp' )
    
    # Name our light
    if not name is None:
        newLight.name = name.value



    # Get Params
    params = lightElement.getElementsByTagName( 'param' )
    
    attenuationType = 'CONSTANT'
    attenuationScale = 1.0
    #falloffType = 'LINEAR'
    falloffScale = 1.0
    angle = 45.0
    
    for param in params:
        paramData = getParamData( param )
        if ( paramData.name == CP.PN.COLOR ):
            newLight.col = toFloat3( paramData.data )
        elif ( paramData.name == CP.PN.ATTENUATION ):
            attenuationType = paramData.data
        elif ( paramData.name == CP.PN.ATTENUATION_SCALE ):
            attenuationScale = float( paramData.data )
        #elif ( paramData.name == CP.PN.FALLOFF ):
        #    falloffType = paramData.data
        elif ( paramData.name == CP.PN.FALLOFF_SCALE ):
            falloffScale = float( paramData.data )
        elif ( paramData.name == CP.PN.ANGLE ):
            angle = float( paramData.data )
    
    
    # Set energy to 1.0 and distance to 20.0 (default)
    newLight.setEnergy( 1.0 )
    newLight.setDist( 20.0 )
    
    # Set light attenuation
    if ( attenuationType == 'LINEAR' ):
        if ( attenuationScale > 0.0 ):
            dist = 2.0 / attenuationScale
        else:
            dist = 5000.0
        newLight.setDist( dist )
        
    elif ( attenuationType == 'QUADRATIC' ):
        newLight.mode |= Lamp.Modes[ 'Quad' ]
        
        # NOTE: This Quad2 value only applies to the formula used
        # in the blender export to calculate the quadratic attenuation
        # and to the distance value of 20.0 and energy value of 1.0
        quad2Value = ( 1.0 / attenuationScale ) * 0.1
        newLight.setQuad2( quad2Value )
    
    # Specific Spot light parameters
    if ( type == 'SPOT' ):
        
        # Set spot angle
        newLight.setSpotSize( angle )
    
        # Set falloff data
        newLight.setSpotBlend( falloffScale / 128.0 )
    
    return id, newLight



def importCamera( cameraElement ):
        
    name = cameraElement.attributes.getNamedItem( 'name' )
    id = cameraElement.attributes.getNamedItem( 'id' ).value
    if name != None:
        name = name.value
    else:
        name = id
    
    # Create our camera
    newCamera = Camera.New( 'persp', name )
    
    # Get COMMON Profile
    techniqueElements = cameraElement.getElementsByTagName( 'technique' )
    commonProfile = getCommonProfile( techniqueElements )

    # Get optics
    optics = commonProfile.getElementsByTagName( 'optics' )
    if ( len( optics ) > 0 ):
        optics = optics[ 0 ]
        
        # Get Program(s)
        programs = optics.getElementsByTagName( 'program' )
        if programs != None:
            program = programs[ 0 ]
            url = program.attributes.getNamedItem( 'url' )
            if url != None:
                url = url.value
                
                # PERSPECTIVE Camera type
                if ( url == 'PERSPECTIVE' ):
                    paramElements = program.getElementsByTagName( 'param' )
                    for paramElement in paramElements:
                        param = getParamData( paramElement )
                        if ( param.name == CP.PN.YFOV ):
                            yfov = float( param.data )
                            lens = 16.0 / math.tan( yfov * 0.5 * ( 3.1415926 / 180.0 ) )
                            newCamera.setLens( lens )
                        if ( param.name == CP.PN.XFOV ):    # TODO: XFOV is not the same...
                            xfov = float( param.data )
                            lens = 16.0 / math.tan( yfov * 0.5 )
                            newCamera.setLens( lens )
                        if ( param.name == CP.PN.ZNEAR ):
                            znear = float( param.data )
                            newCamera.setClipStart( znear )
                        if ( param.name == CP.PN.ZFAR ):
                            zfar = float( param.data )
                            newCamera.setClipEnd( zfar )
                else:
                    print 'Data for ORTHOGRAPHIC Camera type ignored.'
    
    return id, newCamera

def importLibrary( libNode, filePath ):
    
    global filename
    global library
    global currentScene    
    
    # Get library elements
    libraryElements = libNode.getElementsByTagName( 'library' )
    imageElements = None
    textureElements = None
    materialElements = None
    geometryElement = None
    lightElements = None
    cameraElements = None
    
    for child in libraryElements:
        typeValue = child.attributes.getNamedItem( 'type' ).value
        if ( typeValue == 'IMAGE' ):
            imageElements = child.getElementsByTagName( 'image' )
        elif ( typeValue == 'TEXTURE' ):
            textureElements = child.getElementsByTagName( 'texture' )
        elif ( typeValue == 'MATERIAL' ):
            materialElements = child.getElementsByTagName( 'material' )
        elif ( typeValue == 'GEOMETRY' ):
            geometryElement = child.getElementsByTagName( 'geometry' )
        elif ( typeValue == 'LIGHT' ):
            lightElements = child.getElementsByTagName( 'light' )
        elif ( typeValue == 'CAMERA' ):
            cameraElements = child.getElementsByTagName( 'camera' )
    
    
    # Import library data and put into library dictionary
    if imageElements != None:
        for image in imageElements:
            imageData = importImage( image, filePath )
            if ( imageData[ 1 ] != None ):
                library[ imageData[ 0 ] ] = imageData[ 1 ]
    if textureElements != None:
        for texture in textureElements:
            textureData = importTexture( texture )
            library[ textureData[ 0 ] ] = textureData[ 1 ]
    if materialElements != None:
        for material in materialElements:
            materialData = importMaterial( material )
            library[ materialData[ 0 ] ] = materialData[ 1 ]
    if geometryElement != None:
        for mesh in geometryElement:
            meshData = importGeometry( mesh )
            library[ meshData[ 0 ] ] = 'Mesh', meshData[ 1 ]
    if lightElements != None:
        for light in lightElements:
            lightData = importLight( light )
            library[ lightData[ 0 ] ] = 'Lamp', lightData[ 1 ]
    if cameraElements != None:
        for camera in cameraElements:
            cameraData = importCamera( camera )
            library[ cameraData[ 0 ] ] = 'Camera', cameraData[ 1 ]


""" Import Collada scene into Blender scene """
def importScene( colladaNode ):
    
    global currentScene
    global library
    
    # Build scene
    # TODO: Add option for creating a new scene or import into current scene!
    
    
    # Get <scene> element
    sceneElements = colladaNode.getElementsByTagName( 'scene' )
    sceneElement = None
    if not sceneElements is None:
        sceneElement = sceneElements[ 0 ]
    
    name = sceneElement.attributes.getNamedItem( 'name' )
    if not name is None:
        currentScene.setName( name.value )
    
    
    # Import nodes
    nodeElements = getElements( sceneElement, 'node' )
    if not nodeElements is None:
        for node in nodeElements:
            type = node.attributes.getNamedItem( 'type' )
            if not type is None:
                if type.value == 'JOINT':
                    pass
                else:
                    importNode( None, node )
            else:
                importNode( None, node )
    
    
    # Update scene
    currentScene.update( )

    Blender.Redraw( )
    

def importNode( myParent, thisNode ):
    
    global currentScene
    global library
    
    newObject = None
    
 
    # Create new object in blender
    thisNodeID = thisNode.attributes.getNamedItem( 'id' ).value
    # print '<node id=' + thisNodeID + '>'
    
    
    # Get instance
    instanceElements = getElements( thisNode, 'instance' )
    if len( instanceElements ) > 0:
        instanceElement = instanceElements[ 0 ]
        instanceURL = instanceElement.attributes.getNamedItem( 'url' ).value
        instanceURL = instanceURL[1:]
        
        
        # Get Data object (which is a tuple of ['TYPE', Data ] )
        if library.has_key( instanceURL ):
            data = library[ instanceURL ]
            if not data is None:
                newObject = Object.New( data[ 0 ], thisNodeID )
                newObject.link( data[ 1 ] )
    
    if newObject is None:
        newObject = Object.New( 'Empty', thisNodeID )


    # Get baked transform
    matrixElement = getElements( thisNode, 'matrix' )
    relativeMatrix = Mathutils.Matrix( )
    if len( matrixElement ) > 0:
        matrixElement = matrixElement[ 0 ]
        relativeMatrix = toMatrix4x4( matrixElement )
        newObject.setLocation( relativeMatrix.translationPart() )
    
        # Euler angles now has to be in radians ...
        newObject.setEuler( toEulerAngleInRadians( relativeMatrix.rotationPart().toEuler( ) ) )
        
        
    else:
        
        # Look for unbaked transform
        translationElements = getElements( thisNode, 'translate' )
        rotationElements = getElements( thisNode, 'rotate' )
        scaleElements = getElements( thisNode, 'scale' )

        # Set translation
        translateVec = Mathutils.Vector()
        for translate in translationElements:
            addVec3( translateVec, getVector3( translate ) )
        
        newObject.setLocation( translateVec )
        
        # Set rotation
        rotationEuler = Mathutils.Euler( [ 0.0, 0.0, 0.0 ] )
        for rotate in rotationElements:
            euler = getEuler( rotate )
            rotationEuler.x += euler.x
            rotationEuler.y += euler.y
            rotationEuler.z += euler.z
    
        newObject.setEuler( rotationEuler )
        
        # Set scale value
        for scale in scaleElements:
            value = getVector3( scale )
            newObject.setSize( value.x, value.y, value.z )
        
    
    # Link object to scene
    currentScene.link( newObject )    
    
    # Get other nodes
    childList = []
    nodeElements = getElements( thisNode, 'node' )

    if not nodeElements is None:
        for node in nodeElements:
            type = node.attributes.getNamedItem( 'type' )
            if not type is None:
                if type.value == 'JOINT':
                    pass
                else:
                    childList.append( importNode( newObject, node ) )
            else:
                childList.append( importNode( newObject, node ) )

    
    # Make this new object parent of child objects
    if len( childList ) > 0:
        newObject.makeParent( childList, 0, 1 )

    return newObject
    
def main( filename ):
    
    global library
    global currentScene
    global warnings
    
    currentScene = Scene.GetCurrent( )
    library = dict()
    
    libraryElements = None
    sceneElement = None
    
    # Open file
    
    startTime = Blender.sys.time()
    
    # Build DOM tree
    doc = parse( filename )

    # Get COLLADA element
    collada = doc.firstChild
    
    # Extract filePath from filename
    filePath = Blender.sys.dirname( filename )
    
    
    # Import library
    importLibrary( collada, filePath )
    
    # Import scene hiearchy
    importScene( collada )
    
    
    endTime = Blender.sys.time()    
    
    importTime = endTime - startTime
    print "Import time: %.6f" % ( importTime )
    
    # Handle warnings
    if ( warnings ):
        Draw.PupMenu( 'Warning%t|Some information could not be imported. Check console for details' )

def callback_fileselector( filename ):
    if ( Blender.sys.exists( filename ) == 1 ):
        main( filename )
    else:
        Draw.PupMenu( "ERROR: File does not exist!" )
        print 'File does not exist!'


def ImportGUI( ):
    Window.FileSelector( callback_fileselector, 'Import .dae', '' )
    

if not ( _ERROR == True ):
    ImportGUI()

#main( filename )
