import gtk
import egg.trayicon as trayicon

class PastieTray():

    def __init__(self, image=None):
        self._img = gtk.Image()
        self.tray = None
        self.image_file = image
        
    def create_tray(self):
        self._event_box = gtk.EventBox()
        self.tray = trayicon.TrayIcon('Pastie')
        self._load_image(self.image_file)
        
        self._event_box.add(self._img)
        self.tray.add(self._event_box)

    
    def _load_image(self, location=None):
        if not location:
            location = 'pastie.gif'
        self._img.set_from_file(location)
        self._img.show()
        
    def show_tray(self):
        self.tray.show_all()
        
    def hide_tray(self):
        if self.tray:
            self.t.destory()
    
    def connect(self, event):
        self._event_box.connect("button-press-event", event)
            
"""            
            Here's a quick example:
#! /usr/bin/python

def callback(widget, ev):
  print "Button %i pressed!" % ev.button


tray = egg.trayicon.TrayIcon("TrayIcon")
box = gtk.EventBox()
label = gtk.Label("Click Me!")
box.add(label)
tray.add(box)
tray.show_all()

box.connect("button-press-event", callback)

gtk.main()
"""
