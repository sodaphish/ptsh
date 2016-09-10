print "Content-Type: text/html"
print 
import sys
import os
sys.stderr = sys.stdout

_root='/home/cjs/mine/src/feedcollector'
_webroot=("%s%s%s"%(_root, os.sep, 'webui'))
sys.path.append( _root )

import semfeed
from semfeed.webui import *

webui = WebUI(_webroot)
q = webui.get_var('q')


webui.tokenize('title', 'Page Title')
webui.tokenize('year','2011')
webui.tokenize('copyright', 'C.J. Steele')


print webui.parse('header')

print "coming soon."

print webui.parse('footer')
