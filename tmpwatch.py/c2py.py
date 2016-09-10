#!/usr/bin/env python
#
# partial conversion from C and C++ to Python 
#
# License:      Python
# Author:       Issac Trotts
# Created:      Dec. 2001
# Version:      0.0.1
#
import re, sys, string

def c2py(pyfile, cfile):
  clines = cfile.readlines()
  pylines = []
  for line in clines:
    # semicolons
    line = re.sub(r';', '', line)

    # curly braces
    line_is_lone_left_curly = re.match(r'^\s*{\s*((//.*)|(/\*.*\*/))?$', line)
    if line_is_lone_left_curly:
      pylines[-1] = pylines[-1][:-1] + ':\n'
      continue
    line = re.sub(r'{', ':', line)
    line = re.sub(r'}', '', line)

    # comments
    line = re.sub(r'//', '#', line)

    # etc
    line = re.sub(r'->',        '.',    line)
    line = re.sub(r'::',        '.',    line)
    line = re.sub(r'this',      'self', line)
    line = re.sub(r'const\s*',  '',     line)

    #line_is_blank = re.match(r'^\s*$', line)
    #if not line_is_blank:
      #pylines.append(line)
    pylines.append(line)

  for line in pylines:
    pyfile.write(line)

for cname in sys.argv[1:]:
  pyname = cname + '.py' 
  print 'generating '+pyname+' from '+cname
  cfile = open(cname, 'r')
  pyfile = open(pyname, 'w')
  c2py(pyfile, cfile)
  cfile.close()
  pyfile.close()
