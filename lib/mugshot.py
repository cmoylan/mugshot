# What this file will do:
#
# read a config
# create window
# grab an rss feed at a regular interval
# determine status of build
# if the status is green, all is well
# if its red, show picture of offender, from config
#
# if reload button is pressed, run do it all again

from ConfigParser import ConfigParser
from window import MugshotWindow
import os
import urllib
import xml.etree.ElementTree as ElementTree
import re


PROG_ROOT = os.path.dirname(os.path.realpath(__file__))
OFFENDERS_FILE = 'offenders.cfg'
CRUISE_URL = 'http://ccrb.tii.trb/projects/P2PContent.rss'


class Mugshot:
    """Mugshot

    This program will display the image of the person responsible for
    checking in buggy code.

    Statuses:
    broken -- some of the tests failed, the build is broken.
    possibly_broken -- the build is running or the program is determining
        who to blame.
    not_broken -- all of the tests passed, the build is not broken.

    """

    def __init__(self):
        # Create some attributes
        self.build = None
        self.status = None
        self.offender = None

        # Create the offenders list
        self.offenders = {}
        self.read_config()

        # Set the initial status
        initial = self.get_status()
        self.build = initial['build']
        self.status = initial['status']
        self.offender = initial['offender']

        # Initialize the window and hand over control to gtk.main()
        self.window = MugshotWindow(self)
        self.update_status()
        self.window.main()


    def read_config(self):
        config = ConfigParser()
        config.readfp(open(PROG_ROOT + '/../config/' + OFFENDERS_FILE))

        for user in config.sections():
            self.offenders[user] = {
                'name': config.get(user, 'name'),
                'image': config.get(user, 'image')
            }
            #print user
            #print config.get(user, 'name')
            #print config.get(user, 'image')

        return True


    def update_status(self):
        print 'running update_status'
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

        print "build: %s" % build
        print "status: %s" % status
        print "offender: %s" % offender

        return {
            'build': build,
            'status': status,
            'offender': offender
        }




if __name__ == '__main__':
    MUGSHOT = Mugshot()
