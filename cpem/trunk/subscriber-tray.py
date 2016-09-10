"""
PeerDisk Subscriber Tray (subscriber-tray.py) 

@copyright: Copyright 2011, C.J. Steele, all rights reserved.
@author: C.J. Steele <corey@hostedbycorey.com>
@version: 0.1.9
@summary: provides a tray-app for subscribers to control and monitor their PeerDisk client 
"""

import threading
import time
import gobject
import gtk
import gobject
pygtk.require('2.0')
from subprocess import Popen,PIPE

gobject.threads_init()

class AgentTray(threading.Thread):
  def __init__(self,label):
        super(AgentTray,self).__init__()
        self.statusIcon = gtk.StatusIcon()
        #self.statusIcon.set_from_stock(gtk.STOCK_ABOUT)
        self.statusIcon.set_from_file("")
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("PeerDisk Agent")
        self.statusIcon.connect('activate',self.execute_cb,self)
        self.statusIcon.set_visible(1)
        gtk.main()

  def execute_cb(self,widget,event,data=None):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.show_all()

class MyThread(threading.Thread):
    def __init__(self,label):
        super(MyThread,self).__init__()
        self.label = label
        self.quit = False

    def update_label(self,counter):
        self.label.set_text("Counter: %i" % counter)
        return False

    def run(self):
        counter = 0
        while not self.quit:
            counter += 1
            gobject.idle_add(self.update_label,counter)
            time.sleep(60)

w = gtk.Window()
l = gtk.Label()
w.add(l)
w.show_all()
w.connect("destroy",lambda _: gtk.main_quit())
t = MyThread(l)
t.start()

gtk.main()
t.quit = True
