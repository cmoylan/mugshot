#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import pango
from os import path

PROG_ROOT = path.dirname(path.realpath(__file__))
IMAGE_ROOT = PROG_ROOT + '/../images/'
SUCCESS_IMAGE = 'tick.png'
LOAD_IMAGE = 'refresh.png'
FAIL_IMAGE = 'cross.png'
REFRESH_RATE = 60 # seconds


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
        self.window.set_icon_from_file(IMAGE_ROOT + 'icon.png')
        self.window.maximize()

        # Create the containing element
        self.container = gtk.Table(5, 2, False)
        self.window.add(self.container)

        # Create a reload button and pack it into the box container
        reload_button = gtk.Button('Reload', gtk.STOCK_REFRESH)
        reload_button.connect('clicked', self.reload, None)

        # Row 1 --- build heading
        self.build_label = gtk.Label('Build: ---')
        self.build_label.modify_font(pango.FontDescription('sans 24'))
        self.container.attach(self.build_label, 0, 2, 0, 1, yoptions=gtk.SHRINK, ypadding=5)

        # Row 2 --- status heading
        self.status_label = gtk.Label('Status: ---')
        self.status_label.modify_font(pango.FontDescription('sans 36'))
        self.container.attach(self.status_label, 0, 2, 1, 2, yoptions=gtk.SHRINK)


        # Row 3 --- image which will display the mugshot
        self.mug = gtk.Image()
        self.mug.set_from_file(IMAGE_ROOT + LOAD_IMAGE)
        # TODO: get all this scaling crap working
        #self.load_image = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB)
        #gtk.gdk.pixbuf_new_from_file(PROG_ROOT + '/../images/' + LOAD_IMAGE) \
        #    .scale(self.load_image, scale_y=400, interp_type=INTERP_BILINEAR)
        #self.mug.set_from_pixbug(self.load_image)
        self.container.attach(self.mug, 0, 2, 2, 3)

        # Row 4 --- the offender
        self.offender_label = gtk.Label('---')
        self.offender_label.modify_font(pango.FontDescription('sans 48'))
        self.container.attach(self.offender_label, 0, 2, 3, 4, yoptions=gtk.SHRINK)

        # ROw 5 --- buttons
        fixed = gtk.Fixed()
        # Refresh
        fixed.put(reload_button, 0, 0)
        self.container.attach(fixed, 0, 2, 4, 5, yoptions=gtk.SHRINK)
        # Quit

        # Create a timeout that will update the window at regular intervals
        # NOTE: This is deprecated, but the new way doesn't work
        gtk.timeout_add(REFRESH_RATE * 1000, self.obj.update_status)
        #gtk.timeout_add(REFRESH_RATE * 1000, self.reload, None)

        # Show the window and let the public shaming begin
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
        """Change the status of the Mugshot window

        Arguments:
        build -- the build number
        status -- failed, success, or something else
        offender -- SVN username of the build breaker (default None)

        """
        self.build_label.set_text("P2P.Content %s" % build)
        self.status_label.set_text("Status: %s" % status)

        if status == 'failed':
            # If the buid has failed make the background red and show the offender
            self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65535, 0, 0)) # red

            try:
                name = self.obj.offenders[offender]['name']
                image = self.obj.offenders[offender]['image']
                name = "Broken by: %s" % name
            except KeyError:
                name = 'Manually Requested Build'
                image = FAIL_IMAGE

            self.mug.set_from_file(IMAGE_ROOT + image)
            self.offender_label.set_text(name)

        elif status == 'success':
            # If the build is successful, make the background green and display
            # a success graphic
            self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 65535, 0)) # green

            self.mug.set_from_file(IMAGE_ROOT + SUCCESS_IMAGE)
            self.offender_label.set_text('')

        else:
            # If we get here, it's loading or something went wrong. Reset window
            # color and display some loading graphic
            self.window.modify_bg() # default

            self.mug.set_from_file(IMAGE_ROOT + LOADING_IMAGE)
            self.offender_label.set_text('')

            print 'WARNING: No status in Window#change_status!'


