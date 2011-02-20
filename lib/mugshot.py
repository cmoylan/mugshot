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
CONFIG_FILE = 'config'
CRUISE_URL = 'http://ccrb.tii.trb/projects/P2PContent.rss'


class Mugshot:

    def __init__(self):
        #self.read_config()

        # init window
        #self.hello = MugshotWindow(self)
        #self.hello.main()
        self.get_status()

    def read_config(self):
        config = ConfigParser()
        config.readfp(open(PROG_ROOT + '/../' + CONFIG_FILE))
        print config.sections()
        print '-------------------'
        for section in config.sections():
            print section
            #print config.items(section)
            print config.get(section, 'name')
            print config.get(section, 'image')

    def update_status(self):
        print 'updating status'
        self.hello.change_status('red', 'toast')

    def get_status(self):
        cruise_rss = urllib.urlopen(CRUISE_URL)
        cruise_xml = ElementTree.XML(cruise_rss.read())

        # Path to the correct XML nodes. Individual implementations may vary
        status = cruise_xml.find('channel/item/title').text
        offender = cruise_xml.find('channel/item/description').text

        # Parse out all of the noise with some regexes
        status_re = re.search('build (\w+) (\w+)', status)
        build = status_re.group(1)
        status = status_re.group(2)
        offender = re.search('committed by (\w+)', offender).group(1)

        print "build: %s" % build
        print "status: %s" % status
        print "offender: %s" % offender



if __name__ == '__main__':
    MUGSHOT = Mugshot()
