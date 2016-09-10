#!/usr/bin/python
import pygtk
import vte
import time
pygtk.require('2.0')
import gtk
from subprocess import Popen, PIPE

class NInfoTray:
  def __init__(self):
    self.statusIcon = gtk.StatusIcon()
    #self.statusIcon.set_from_stock(gtk.STOCK_ABOUT)
    self.statusIcon.set_from_file("network.svg")
    self.statusIcon.set_visible(True)
    self.statusIcon.set_tooltip("Network Information")
    self.statusIcon.connect('activate', self.execute_cb, self)
    self.statusIcon.set_visible(1)
    gtk.main()


  def execute_cb(self, widget, event, data = None):
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    #window.set_resizable( False )
		#window = gtk.Window()
		#window.connect('destroy', lambda w: gtk.main_quit())
		#terminal = vte.Terminal()
		#terminal.fork_command( '/home/cjs/bin/ninfo 1')
		#terminal.connect('show', self.execute_cb, self)
		#window.add(terminal)
		window.show_all()



if __name__ == "__main__":
  ninfo = NInfoTray()
