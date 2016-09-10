"""
WebUI class - simple web templating engine with tokens 
	Copyright 2011, C.J. Steele, all rights reserved.
"""
import cgi 
import sys
import os
import semfeed
from string import Template

class WebUI():
	root = None
	template = None
	tokens = {}

	def __init__(self, rootdir, templatedir='templates'):
		self.set_root_dir(rootdir)
		self.set_template_dir(templatedir)

	def set_root_dir(self, rootdir):
		if os.path.exists(rootdir):
			self.root=rootdir
		else:
			raise OSError, "file not found"
		
	def set_template_dir(self, templatedir='templates'):
		templatedir="%s%s%s"%(self.root, os.sep, templatedir)
		if os.path.exists(templatedir):
			self.template=templatedir
		else:
			raise OSError, "file not found (%s)"%(templatedir)

	def get_template(self, template_name):
		template_file = "%s%s%s.t"%(self.template, os.sep, template_name)
		if os.path.exists(template_file):
			contents = None
			with open(template_file) as f:
				contents=f.read()
			return Template(contents)
		else:
			raise OSError, "file not found"

	def add_token(self,key,name):
		self.tokenize(key,name)

	def tokenize(self, key, name):
		self.tokens[key]=name

	def dump_tokens(self,**kwargs):
		for token in self.tokens:
			print "%s: %s"%(k, self.tokens[k])

	def parse(self, templatename):
		t = self.get_template(templatename)
		#if kwargs is not None:
		#	t.substitute(kwargs)
		return t.substitute(self.tokens)

	def get_var(self, keyname):
		#TODO: sanitize input to make sure no XSS and now SQL mangling
		form = cgi.FieldStorage()
		if keyname in form:
			return form[keyname].value
		else:
			return None
