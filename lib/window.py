#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import pango
from os import path

PROG_ROOT = path.dirname(path.realpath(__file__))

class MugshotWindow:

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
        self.window.set_title("Mugshot")
        #red = gtk.gdk.color_parse('#000000')
        #self.window.set_background(red)
        # self.window.set_icon_from_file(some icon)
        self.window.maximize()

        # Create the containing element
        self.container = gtk.Table(5, 2, False)
        self.window.add(self.container)
        #col_1 = self.container.get_column_at_index(1)
        #col_1.width_request(0)

        # Create a reload button and pack it into the box container
        reload_button = gtk.Button('Reload', gtk.STOCK_REFRESH)
        reload_button.connect('clicked', self.reload, None)
        #reload_button.set_size_request(0, 0)
        #self.container.attach(reload_button, 1, 2, 0, 1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK, ypadding=-1)

        # Row 1 --- build heading
        self.build_label = gtk.Label('Build: 123456789')
        self.container.attach(self.build_label, 0, 2, 0, 1, yoptions=gtk.SHRINK)

        # Row 2 --- status heading
        self.status_label = gtk.Label('Status: Not Broken')
        self.status_label.modify_font(pango.FontDescription('sans 24'))
        self.container.attach(self.status_label, 0, 2, 1, 2)


        # Row 3 --- image which will display the mugshot
        self.mug = gtk.Image()
        self.mug.set_from_file(PROG_ROOT + '/../images/arduino.jpg')
        self.container.attach(self.mug, 0, 2, 2, 3)

        # Row 4 --- the offender
        self.offender_label = gtk.Label('chris moylan')
        self.offender_label.modify_font(pango.FontDescription('sans 48'))
        #self.offender_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(65535,0,0))
        self.container.attach(self.offender_label, 0, 2, 3, 4, yoptions=gtk.SHRINK)

        # ROw 5 --- buttons
        fixed = gtk.Fixed()
        # Refresh
        fixed.put(reload_button, 0, 0)
        self.container.attach(fixed, 0, 2, 4, 5, yoptions=gtk.SHRINK)
        # Quit

        # Create a timeout that will update the window at regular intervals
        # NOTE: This is deprecated, but the new way doesn't work
        #gtk.timeout_add(2000, self.obj.update_status)

        # Display the remaining hidden UI elements
        self.window.show_all()


    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()


    # --- Callbacks ---
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


    def reload(self, widget, data=None):
        self.obj.update_status()


    # --- Non-callback methods, called from the mugshot.py ---
    def change_status(self, build, status, offender=None):
        self.build_label.set_text("P2P.Content %s" % build)
        self.status_label.set_text("Status: %s" % status)

        if status == 'failed':
            # If the buid has failed make the background red and show the offender
            self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65535, 0, 0)) # red
            # display the offender image
            # display full name
            self.offender_label.set_text(offender)
        elif status == 'success':
            # If the build is successful, make the background green and display
            # a success graphic
            self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 65535, 0)) # green
            # display success graphic
            self.offender_label.set_text('')
        else:
            # If we get here, it's loading or something went wrong
            # Display some loading graphic
            self.offender_label.set_text('')
            print 'WARNING: No status in Window#change_status!'




