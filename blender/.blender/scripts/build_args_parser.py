# -*- coding:utf-8 -*-
import os
import sys

def parse(arg_config):
	res = {}
	argv = sys.argv # python2
	print("send sys.argv =", argv)
	i = 0
	while i < len(argv):
		s = argv[i]
		i = i + 1
		if s.find('-') != -1:
			arg_name = s.replace('-', '')
			arg_type = arg_config.get(arg_name, None)
			value = None
			if (arg_type == None) or (i >= len(argv)):
				continue
			if arg_type is dict:
				print("cannot support type 'dict' argv[%s]=%s" % (i, arg_name))
				return {}
			elif arg_type is list: # 只允许list<string>
				value = []
				while i < len(argv) and argv[i].find('-') == -1:
					value.append(argv[i])
					i = i + 1
			else:
				value = argv[i]
			if arg_type is int:
				if value == None:
					value = -1
				else:
					value = int(value)
			elif arg_type is bool:
				if value == None:
					value = False
				else:
					value = value.lower() == "true" and True or False
			elif arg_type is str:
				if value == None:
					value = ""
			res[arg_name] = value
			i = i + 1
	return res