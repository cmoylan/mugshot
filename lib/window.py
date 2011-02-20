#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os

PROG_ROOT = os.path.dirname(os.path.realpath(__file__))

class MugshotWindow:

    # Mocked function to change the status of the build
    def change_status(self, status, blame=None):
        # If status is green, make the background green
        # If status is red, make the background red and display blame image
        if status == 'red':
            self.mug.set_from_file(PROG_ROOT + '/../images/homemade-arduino-kindof.jpg')
            self.mug.show()
        else:
            pass

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    #def hello(self, widget, data=None):
    #    print "Hello World"
    #    self.toast()

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self, obj):
        # sometimes the window needs to interact with the mugshot object.
        # Therefore, make a reference back to the mugshot object from within
        # the window class
        self.obj = obj

        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        # Set basic window attributes
        self.window.set_border_width(10)
        self.window.set_title("kobe")
        #red = gtk.gdk.color_parse('#000000')
        #self.window.set_background(red)
        # self.window.set_icon_from_file(some icon)
        self.window.maximize()

        # Create a box container and attach it to the window
        self.box1 = gtk.HBox(False, 0)
        self.window.add(self.box1)

        # Creates a new button with the label "Hello World".
        #self.button = gtk.Button("Hello World")

        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        #self.button.connect("clicked", self.hello, None)

        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        #self.button.connect_object("clicked", gtk.Widget.destroy, self.window)

        # This packs the button into the window (a GTK container).
        #self.window.add(self.button)
        #self.box1.pack_start(self.button, True, True, 0)

        # The final step is to display this newly created widget.
        #self.button.show()

        self.reload_button = gtk.Button('Reload')
        self.reload_button.connect('clicked', self.reload, None)
        self.box1.pack_start(self.reload_button)
        self.reload_button.show()

        self.mug = gtk.Image()
        self.mug.set_from_file(PROG_ROOT + '/../images/arduino.jpg')
        self.box1.add(self.mug)
        self.mug.show()

        # show the box
        self.box1.show()

        # and the window
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

    def reload(self, widget, data=None):
        self.obj.update_status()

