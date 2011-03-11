from ConfigParser import ConfigParser
from window import MugshotWindow
from os import path
import urllib
import xml.etree.ElementTree as ElementTree
import re
import random
#from time import sleep


PROG_ROOT = path.dirname(path.realpath(__file__))
CONFIG_ROOT = PROG_ROOT + '/../config/'
CONFIG_FILE = 'options.cfg'
OFFENDERS_FILE = 'offenders.cfg'
DEBUG = False

CRUISE_URL = 'http://ccrb.tii.trb/projects/P2PContent.rss'


class Mugshot:
    """Main Mugshot object

    This program will display the image of the person responsible for
    checking in buggy code. It's like CCMenu, but it hurts your feelings.

    Statuses:
    success -- some of the tests failed, the build is broken.
    unknown -- the build is running or the program is determining
        who to blame.
    failed -- all of the tests passed, the build is not broken.

    """

    def __init__(self):
        """Constructor

        Get the build status and initialize the Window object

        """
        # Create some attributes
        self.options = {}
        self.build = None
        self.status = None
        self.offender = None

        # Load the config
        self.load_config()

        # Create the offenders list
        self.offenders = {}
        self.parse_offenders()

        # Set the initial status
        initial = self.get_status()
        self.build = initial['build']
        self.status = initial['status']
        self.offender = initial['offender']

        # Initialize the window and hand over control to gtk.main()
        self.window = MugshotWindow(self)
        self.update_status()
        self.window.main()
        self.load_config()


    def load_config(self):
        """Load the config file and setup some instance variables

        """
        global CRUISE_URL

        config = ConfigParser()
        config.readfp(open(PROG_ROOT + '/../config/' + CONFIG_FILE))

        sections = config.sections()
        print sections

        if 'settings' in sections:
            CRUISE_URL = 'http://' + config.get('settings', 'cruise_url')

        if 'images' in sections:
            self.options['success_images'] = config.get('images', 'success').split(',')
            self.options['fail_images'] = config.get('images', 'fail').split(',')
            self.options['load_images'] = config.get('images', 'load').split(',')


    def parse_offenders(self):
        """Generate the list of offenders

        Looks up the offenders.ini file, and parses it into an array of hashes

        """
        config = ConfigParser()
        config.readfp(open(CONFIG_ROOT + OFFENDERS_FILE))

        for user in config.sections():
            self.offenders[user] = {
                'name': config.get(user, 'name'),
                'image': config.get(user, 'image')
            }

            if DEBUG:
                print user
                print config.get(user, 'name')
                print config.get(user, 'image')

        return True


    def update_status(self):
        """Update the status window

        Retrieves the build status and sends this to the Window object. This
        can be called from within Mugshot or Window

        """
        if self.status is None:
            # Something is wrong, it should never get here
            print 'ERROR, ERROR: self.status is None...this should not happen'
            return False

        current_build = self.get_status()
        #if current_build['build'] == self.build:
            # The build hasn't changed, do nothing more
            #return False

        self.build = current_build['build']
        self.status = current_build['status']
        self.offender = current_build['offender']

        # Update the window
        self.window.change_status(self.build, self.status, self.offender)

        return True


    def get_status(self):
        """Retreives the status from the CI server

        Hits the URL for the RSS feed from Cruise and parses out the status of
        the build and the offender, if it is broken

        """
        # TODO: If multiple checkins are built together, there might be
        # multiple regex matches. Hopefully the regex is not greedy
        cruise_rss = urllib.urlopen(CRUISE_URL)
        cruise_xml = ElementTree.XML(cruise_rss.read())

        # Path to the correct XML nodes. Individual implementations may vary
        status_xml = cruise_xml.find('channel/item/title').text
        offender_xml = cruise_xml.find('channel/item/description').text

        # Parse out all of the noise with some regexes
        status_re = re.search('build ([0-9]*\.[0-9]+|[0-9]+) (\w+)', status_xml)

        if status_re is not None:
            build = status_re.group(1)
            status = status_re.group(2)
        else:
            build = 'unknown'
            status = 'unknown'

        try:
            offender = re.search('committed by (\w+)', offender_xml).group(1)
        except:
            offender = None

        if DEBUG:
            print "build: %s" % build
            print "status: %s" % status
            print "offender: %s" % offender

        return {
            'build': build,
            'status': status,
            'offender': offender
        }


    def get_image(self, status):
        """Return a random image for the status

        Arguments:
        status -- a string representing the status

        Returns:
        A string representing the image

        """
        # TODO: this should use the internal self.status instead of accepting a
        #       status argument
        key = 'load'

        if status:
            if status == 'success':
                key = 'success'
            elif status == 'failed':
                key = 'fail'
        else:
            # Get the value from self
            pass

        return random.choice(self.options[key + '_images'])


    def demo(self):
        """Plays a short demo

        Loops through all of the offenders and displays their mugshots briefly

        """
        #for offender in self.offenders:
            #self.window.change_status('*DEMO MODE*', 'failed', offender)
            #sleep(2)
        pass




if __name__ == '__main__':
    MUGSHOT = Mugshot()
