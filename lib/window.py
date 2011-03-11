#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import pango
from os import path

PROG_ROOT = path.dirname(path.realpath(__file__))
IMAGE_ROOT = PROG_ROOT + '/../images/'
#SUCCESS_IMAGE = 'tick.png'
#LOAD_IMAGE = 'refresh.png'
#FAIL_IMAGE = 'cross.png'
REFRESH_RATE = 10 # seconds

# Define colors
BLACK = gtk.gdk.color_parse('#000')
RED = gtk.gdk.color_parse('#ff0000')
GREEN = gtk.gdk.color_parse('#00ff00')


class MugshotWindow:

    def __init__(self, obj):
        """Initialize the Mugshot window

        Required Arguments:
        obj -- The calling object. This should always be an instance of
            the MugShot class.

        """
        # Make a reference back to the calling object so that we can 
        # interact with it.
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
        container = gtk.Table(5, 2, False)
        self.window.add(container)

        # Row 1 --- build heading
        self.build_label = gtk.Label('Build: ---')
        self.build_label.modify_fg(gtk.STATE_NORMAL, BLACK)
        self.build_label.modify_font(pango.FontDescription('sans 24'))
        container.attach(self.build_label, 0, 2, 0, 1, yoptions=gtk.SHRINK, ypadding=5)

        # Row 2 --- status heading
        self.status_label = gtk.Label('Status: ---')
        self.status_label.modify_fg(gtk.STATE_NORMAL, BLACK)
        self.status_label.modify_font(pango.FontDescription('sans 36'))
        container.attach(self.status_label, 0, 2, 1, 2, yoptions=gtk.SHRINK)


        # Row 3 --- image which will display the mugshot
        self.mug = gtk.Image()
        self.mug.set_from_file(IMAGE_ROOT + self.obj.get_image('load'))
        # TODO: get all this scaling crap working
        #self.load_image = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB)
        #gtk.gdk.pixbuf_new_from_file(PROG_ROOT + '/../images/' + LOAD_IMAGE) \
        #    .scale(self.load_image, scale_y=400, interp_type=INTERP_BILINEAR)
        #self.mug.set_from_pixbug(self.load_image)
        container.attach(self.mug, 0, 2, 2, 3)

        # Row 4 --- the offender
        self.offender_label = gtk.Label('---')
        self.offender_label.modify_fg(gtk.STATE_NORMAL, BLACK)
        self.offender_label.modify_font(pango.FontDescription('sans 48'))
        container.attach(self.offender_label, 0, 2, 3, 4, yoptions=gtk.SHRINK)

        # ROw 5 --- buttons
        box = gtk.HBox()
        # Reload
        reload_button = gtk.Button('Reload', gtk.STOCK_REFRESH)
        reload_button.connect('clicked', self.reload, None)
        box.pack_end(reload_button, False, False)
        # Demo
        #demo_button = gtk.Button('Demo')
        #demo_button.connect('clicked', self.obj.demo, None)
        #box.pack_end(demo_button, False, False, 5)
        # Quit
        quit_button = gtk.Button('Quit', gtk.STOCK_QUIT)
        quit_button.connect('clicked', self.destroy, None)
        box.pack_end(quit_button, False, False, 5)

        # Place box into table
        container.attach(box, 0, 2, 4, 5, yoptions=gtk.SHRINK)

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
        """Destroy the window

        """
        print "destroy signal occurred"
        gtk.main_quit()


    def reload(self, widget, data=None):
        """Manually reload the window

        Callback for the Reload button

        """
        self.obj.update_status()


    def demo(self, widget, data=None):
        self.obj.demo()


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
            self.window.modify_bg(gtk.STATE_NORMAL, RED) # red

            try:
                name = self.obj.offenders[offender]['name']
                image = self.obj.offenders[offender]['image']
                name = "Broken by: %s" % name
            except KeyError:
                name = 'Manually Requested Build'
                image = self.obj.get_image('failed')

            self.mug.set_from_file(IMAGE_ROOT + image)
            self.offender_label.set_text(name)

        elif status == 'success':
            # If the build is successful, make the background green and display
            # a success graphic
            self.window.modify_bg(gtk.STATE_NORMAL, GREEN) # green

            self.mug.set_from_file(IMAGE_ROOT + self.obj.get_image('success'))
            self.offender_label.set_text('')

        else:
            # If we get here, it's loading or something went wrong. Reset window
            # color and display some loading graphic
            self.window.modify_bg() # default

            self.mug.set_from_file(IMAGE_ROOT + self.obj.get_image('load'))
            self.offender_label.set_text('')

            print 'WARNING: No status in Window#change_status!'


