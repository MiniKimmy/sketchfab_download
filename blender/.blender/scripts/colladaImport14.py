#!BPY

"""
Name: 'COLLADA 1.4(.dae) ...'
Blender: 241
Group: 'Import'
Tooltip: 'Import scene from COLLADA 1.4 format (.dae)'
"""

__author__ = "Illusoft - Pieter Visser"
__url__ = ("Project homepage, http://colladablender.illusoft.com")
__version__ = "0.3.160"
__email__ = "colladablender@illusoft.com"
__bpydoc__ = """\

Description: Imports a COLLADA 1.4 file into a Blender scene.

Bugs and Features: check the project website: http://colladablender.illusoft.com

Usage: Run the script from the menu or inside Blender.
"""

# --------------------------------------------------------------------------
# Illusoft Collada 1.4 plugin for Blender
# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2006: Illusoft - colladablender@illusoft.com
# 2008.05.08 modif. for debug mode by migius (AKA Remigiusz Fiedler)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

import sys
import Blender

error = False

######################## SET PATH TO FOLDER consisting 'colladaImEx' here (if necessary)

# Example:

# scriptsDir = "C:/Temp/"

scriptsDir = ""

#############################################################################

try:
	import colladaImEx.cstartup
	if Blender.Get('scriptsdir') is None and Blender.Get('uscriptsdir') is None:
		if scriptsDir == '' or scriptsDir is None:
			Blender.Draw.PupMenu("Cannot find folder %t | Please set path in file 'colladaImport14.py'")
			error = True
		else:
			loc = scriptsDir
	else:
		loc = ""
except ImportError:
	# Check if full version of python is installed:
	try:
		import os
		pythonFull = True
	except ImportError:
		pythonFull = False

	if not pythonFull:
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
		Blender.Draw.PupMenu("Please install full version of python %t | Check the console for more info")
		error = True
	else:
		if scriptsDir == "":
			Blender.Draw.PupMenu("Cannot find folder %t | Please set path in file 'colladaImport14.py'")
			error = True
		else:
			if scriptsDir not in sys.path:
				sys.path.append(scriptsDir)
			try:
				import colladaImEx.cstartup
				loc = scriptsDir
			except:
				Blender.Draw.PupMenu("Cannot find colladaImEx files %t | Please make sure the path is correct in file 'colladaImport14.py'")
				error = True
except StandardError:
	error = True

debug = False #or True
if debug:
	#hack for debug outputs to the console
	reload(colladaImEx.cstartup)
	colladaImEx.cstartup.Main(True, loc)
elif not error:
	try:
		reload(colladaImEx.cstartup)
		colladaImEx.cstartup.Main(True, loc)
	except StandardError:
		pass

"""a try to receive error messages to the console:
except:
	print 'deb: PROBLEM !!!!!' #-------
	#print sys.exc_info()[1]
	#print sys.exc_info()
	print sys.exc_type, sys.exc_value #-------
	#traceback.print_exc(file=sys.stdout)
"""
